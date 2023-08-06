import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Union

import asyncpg

from abrechnung.domain.accounts import Account, AccountType, AccountDetails
from abrechnung.util import parse_postgres_datetime
from . import (
    Application,
    NotFoundError,
    check_group_permissions,
    InvalidCommand,
    create_group_log,
)
from ..domain.users import User


@dataclass
class RawAccount:
    id: int
    group_id: int
    name: str
    description: str
    priority: int
    owning_user_id: Optional[int]
    deleted: bool
    type: Optional[str] = field(default=None)
    clearing_shares: Optional[dict[int, float]] = field(default=None)


class AccountService(Application):
    @staticmethod
    async def _increment_account_version(conn: asyncpg.Connection, revision_id: int):
        await conn.execute(
            "update account_revision set version = version + 1 where id = $1",
            revision_id,
        )

    @staticmethod
    async def _get_or_create_revision(
        conn: asyncpg.Connection, user: User, account_id: int
    ) -> int:
        """return the revision id, assumes we are already in a transaction"""
        revision_id = await conn.fetchval(
            "select id "
            "from account_revision "
            "where account_id = $1 and user_id = $2 and committed is null",
            account_id,
            user.id,
        )
        if revision_id:  # there already is a wip revision
            return revision_id

        # create a new transaction revision
        revision_id = await conn.fetchval(
            "insert into account_revision (user_id, account_id) values ($1, $2) returning id",
            user.id,
            account_id,
        )
        return revision_id

    @staticmethod
    async def _check_account_permissions(
        conn: asyncpg.Connection,
        user: User,
        account_id: int,
        can_write: bool = False,
        account_type: Optional[Union[str, list[str]]] = None,
    ) -> tuple[int, str]:
        """returns group id of the transaction"""
        result = await conn.fetchrow(
            "select a.type, a.group_id, can_write, is_owner "
            "from group_membership gm join account a on gm.group_id = a.group_id and gm.user_id = $1 "
            "where a.id = $2",
            user.id,
            account_id,
        )
        if not result:
            raise NotFoundError(f"account not found")

        if can_write and not (result["can_write"] or result["is_owner"]):
            raise PermissionError(f"user does not have write permissions")

        if account_type:
            type_check = (
                [account_type] if isinstance(account_type, str) else account_type
            )
            if result["type"] not in type_check:
                raise InvalidCommand(
                    f"Transaction type {result['type']} does not match the expected type {type_check}"
                )

        return result["group_id"], result["type"]

    async def _get_or_create_pending_account_change(
        self, conn: asyncpg.Connection, user: User, account_id: int
    ) -> int:
        revision_id = await self._get_or_create_revision(
            conn=conn, user=user, account_id=account_id
        )

        a = await conn.fetchval(
            "select id from account_history th where revision_id = $1 and id = $2",
            revision_id,
            account_id,
        )
        if a:
            return revision_id

        last_committed_revision = await conn.fetchval(
            "select ar.id "
            "from account_revision ar "
            "   join account_history ah on ar.id = ah.revision_id and ar.account_id = ah.id "
            "where ar.account_id = $1 and ar.committed is not null "
            "order by ar.committed desc "
            "limit 1",
            account_id,
        )

        if last_committed_revision is None:
            raise InvalidCommand(
                f"Cannot edit account {account_id} as it has no committed changes."
            )

        # copy all existing transaction data into a new history entry
        await conn.execute(
            "insert into account_history (id, revision_id, name, description, priority, deleted)"
            "select id, $1, name, description, priority, deleted "
            "from account_history where id = $2 and revision_id = $3",
            revision_id,
            account_id,
            last_committed_revision,
        )

        # copy all last committed creditor shares
        await conn.execute(
            "insert into clearing_account_share (account_id, revision_id, share_account_id, shares) "
            "select account_id, $1, share_account_id, shares "
            "from clearing_account_share where account_id = $2 and revision_id = $3",
            revision_id,
            account_id,
            last_committed_revision,
        )

        return revision_id

    @staticmethod
    async def _check_account_exists(
        conn: asyncpg.Connection, group_id: int, account_id: int
    ) -> int:
        acc = await conn.fetchval(
            "select account_id from committed_account_state_valid_at() "
            "where group_id = $1 and account_id = $2 and not deleted",
            group_id,
            account_id,
        )
        if not acc:
            raise NotFoundError(f"Account with id {account_id}")

        return True

    async def _account_clearing_shares_check(
        self,
        conn: asyncpg.Connection,
        user: User,
        account_id: int,
        share_account_id: int,
        account_type: Optional[Union[str, list[str]]] = None,
    ) -> tuple[int, int]:
        """returns tuple of group_id of the account and the users revision_id of the pending change"""
        group_id, _ = await self._check_account_permissions(
            conn=conn,
            user=user,
            account_id=account_id,
            can_write=True,
            account_type=account_type,
        )

        await self._check_account_exists(conn, group_id, share_account_id)

        revision_id = await self._get_or_create_pending_account_change(
            conn=conn, user=user, account_id=account_id
        )

        return group_id, revision_id

    @staticmethod
    def _account_detail_from_db_json(db_json: dict) -> AccountDetails:
        return AccountDetails(
            name=db_json["name"],
            description=db_json["description"],
            deleted=db_json["deleted"],
            priority=db_json["priority"],
            owning_user_id=db_json["owning_user_id"],
            revision_started_at=parse_postgres_datetime(db_json["revision_started"]),
            revision_committed_at=None
            if db_json.get("revision_committed") is None
            else parse_postgres_datetime(db_json["revision_committed"]),
            clearing_shares={
                cred["share_account_id"]: cred["shares"]
                for cred in db_json["clearing_shares"]
            },
            changed_by=db_json["changed_by"],
        )

    def _account_db_row(self, account: asyncpg.Record) -> Account:
        committed_details = (
            self._account_detail_from_db_json(
                json.loads(account["committed_details"])[0]
            )
            if account["committed_details"]
            else None
        )
        pending_details = (
            self._account_detail_from_db_json(json.loads(account["pending_details"])[0])
            if account["pending_details"]
            else None
        )

        return Account(
            id=account["account_id"],
            group_id=account["group_id"],
            type=account["type"],
            is_wip=account["is_wip"],
            last_changed=account["last_changed"],
            version=account["version"],
            committed_details=committed_details,
            pending_details=pending_details,
        )

    async def list_accounts(self, *, user: User, group_id: int) -> list[Account]:
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                await check_group_permissions(conn=conn, group_id=group_id, user=user)
                cur = conn.cursor(
                    "select account_id, group_id, type, last_changed, version, is_wip, "
                    "   committed_details, pending_details "
                    "from full_account_state_valid_at($1) "
                    "where group_id = $2",
                    user.id,
                    group_id,
                )

                result = []
                async for account in cur:
                    result.append(self._account_db_row(account))

                return result

    async def get_account(self, *, user: User, account_id: int) -> Account:
        async with self.db_pool.acquire() as conn:
            await self._check_account_permissions(
                conn=conn, user=user, account_id=account_id
            )
            account = await conn.fetchrow(
                "select account_id, group_id, type, last_changed, version, is_wip, "
                "   committed_details, pending_details "
                "from full_account_state_valid_at($1) "
                "where account_id = $2",
                user.id,
                account_id,
            )
            return self._account_db_row(account)

    async def _create_account(
        self,
        *,
        conn: asyncpg.Connection,
        user: User,
        group_id: int,
        type: str,
        name: str,
        description: str,
        owning_user_id: Optional[int] = None,
        priority: int = 0,
        clearing_shares: Optional[dict[int, float]] = None,
    ) -> int:
        if clearing_shares and type != AccountType.clearing.value:
            raise InvalidCommand(
                f"'{type}' accounts cannot have associated settlement distribution shares"
            )

        can_write, is_owner = await check_group_permissions(
            conn=conn, group_id=group_id, user=user, can_write=True
        )
        if owning_user_id is not None:
            if not is_owner and owning_user_id != user.id:
                raise PermissionError(
                    f"only group owners can associate others with accounts"
                )

        account_id = await conn.fetchval(
            "insert into account (group_id, type) values ($1, $2) returning id",
            group_id,
            type,
        )

        revision_id = await self._get_or_create_revision(conn, user, account_id)
        await conn.execute(
            "insert into account_history (id, revision_id, name, description, owning_user_id, priority) "
            "values ($1, $2, $3, $4, $5, $6)",
            account_id,
            revision_id,
            name,
            description,
            owning_user_id,
            priority,
        )
        if clearing_shares and type == AccountType.clearing.value:
            # TODO: make this more efficient
            for share_account_id, value in clearing_shares.items():
                if value == 0:
                    continue
                await self._check_account_exists(conn, group_id, share_account_id)
                await conn.execute(
                    "insert into clearing_account_share (account_id, revision_id, share_account_id, shares) "
                    "values ($1, $2, $3, $4)",
                    account_id,
                    revision_id,
                    share_account_id,
                    value,
                )

        await create_group_log(
            conn=conn,
            group_id=group_id,
            user=user,
            type="account-committed",
            message=f"created account {name}",
        )
        await conn.execute(
            "update account_revision set committed = now() where id = $1",
            revision_id,
        )
        return account_id

    async def create_account(
        self,
        *,
        user: User,
        group_id: int,
        type: str,
        name: str,
        description: str,
        owning_user_id: Optional[int] = None,
        priority: int = 0,
        clearing_shares: Optional[dict[int, float]] = None,
    ) -> int:
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                return await self._create_account(
                    conn=conn,
                    user=user,
                    group_id=group_id,
                    type=type,
                    name=name,
                    description=description,
                    owning_user_id=owning_user_id,
                    priority=priority,
                    clearing_shares=clearing_shares,
                )

    async def _update_account(
        self,
        conn: asyncpg.Connection,
        user: User,
        account_id: int,
        name: str,
        description: str,
        owning_user_id: Optional[int] = None,
        priority: int = 0,
        clearing_shares: Optional[dict[int, float]] = None,
    ):
        group_id, account_type = await self._check_account_permissions(
            conn=conn, user=user, account_id=account_id, can_write=True
        )
        can_write, is_owner = await check_group_permissions(
            conn=conn, group_id=group_id, user=user, can_write=True
        )
        if clearing_shares and account_type != AccountType.clearing.value:
            raise InvalidCommand(
                f"'{account_type}' accounts cannot have associated settlement distribution shares"
            )

        revision_id = await self._get_or_create_revision(
            conn=conn, user=user, account_id=account_id
        )

        committed_account = await conn.fetchrow(
            "select owning_user_id from committed_account_state_valid_at() where account_id = $1",
            account_id,
        )

        if owning_user_id is not None:
            if not is_owner and owning_user_id != user.id:
                raise PermissionError(
                    f"only group owners can associate others with accounts"
                )
        elif (
            committed_account["owning_user_id"] is not None
            and committed_account["owning_user_id"] != user.id
            and not is_owner
        ):
            raise PermissionError(
                f"only group owners can remove other users as account owners"
            )

        await conn.execute(
            "insert into account_history (id, revision_id, name, description, owning_user_id, priority) "
            "values ($1, $2, $3, $4, $5, $6) ",
            account_id,
            revision_id,
            name,
            description,
            owning_user_id,
            priority,
        )
        if clearing_shares and account_type == AccountType.clearing.value:
            # TODO: make this more efficient
            for share_account_id, value in clearing_shares.items():
                if value == 0:
                    continue
                await self._check_account_exists(conn, group_id, share_account_id)
                await conn.execute(
                    "insert into clearing_account_share (account_id, revision_id, share_account_id, shares) "
                    "values ($1, $2, $3, $4)",
                    account_id,
                    revision_id,
                    share_account_id,
                    value,
                )

        await self._increment_account_version(conn=conn, revision_id=revision_id)
        await create_group_log(
            conn=conn,
            group_id=group_id,
            user=user,
            type="account-committed",
            message=f"updated account {name}",
        )
        await conn.execute(
            "update account_revision set committed = now() where id = $1",
            revision_id,
        )

    async def update_account(
        self,
        user: User,
        account_id: int,
        name: str,
        description: str,
        owning_user_id: Optional[int] = None,
        priority: int = 0,
        clearing_shares: Optional[dict[int, float]] = None,
    ):
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                return await self._update_account(
                    conn=conn,
                    user=user,
                    account_id=account_id,
                    name=name,
                    description=description,
                    owning_user_id=owning_user_id,
                    priority=priority,
                    clearing_shares=clearing_shares,
                )

    async def delete_account(
        self,
        user: User,
        account_id: int,
    ):
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                group_id, _ = await self._check_account_permissions(
                    conn=conn, user=user, account_id=account_id, can_write=True
                )
                row = await conn.fetchrow(
                    "select id from account where id = $1",
                    account_id,
                )
                if row is None:
                    raise InvalidCommand(f"Account does not exist")

                has_committed_shares = await conn.fetchval(
                    "select 1 "
                    "from committed_transaction_state_valid_at() t "
                    "where not deleted and $1 = any(involved_accounts)",
                    account_id,
                )
                has_pending_shares = await conn.fetchval(
                    "select 1 "
                    "from aggregated_pending_transaction_history t "
                    "where $1 = any(t.involved_accounts)",
                    account_id,
                )

                has_committed_usages = await conn.fetchval(
                    "select 1 "
                    "from committed_transaction_position_state_valid_at() p "
                    "join transaction t on t.id = p.transaction_id "
                    "where not p.deleted and $1 = any(p.involved_accounts)",
                    account_id,
                )

                has_pending_usages = await conn.fetchval(
                    "select 1 "
                    "from aggregated_pending_transaction_position_history p "
                    "join transaction t on t.id = p.transaction_id "
                    "where $1 = any(p.involved_accounts)",
                    account_id,
                )

                if (
                    has_committed_shares
                    or has_pending_shares
                    or has_committed_usages
                    or has_pending_usages
                ):
                    raise InvalidCommand(
                        f"Cannot delete an account that is references by a transaction"
                    )

                row = await conn.fetchrow(
                    "select name, revision_id, deleted "
                    "from committed_account_state_valid_at() "
                    "where account_id = $1",
                    account_id,
                )
                if row is None:
                    raise InvalidCommand(
                        f"Cannot delete an account without any committed changes"
                    )

                if row["deleted"]:
                    raise InvalidCommand(f"Cannot delete an already deleted account")

                has_committed_clearing_shares = await conn.fetchval(
                    "select 1 "
                    "from committed_account_state_valid_at() p "
                    "where not p.deleted and $1 = any(p.involved_accounts)",
                    account_id,
                )

                has_pending_clearing_shares = await conn.fetchval(
                    "select 1 "
                    "from aggregated_pending_account_history p "
                    "where $1 = any(p.involved_accounts)",
                    account_id,
                )
                if has_committed_clearing_shares or has_pending_clearing_shares:
                    raise InvalidCommand(
                        f"Cannot delete an account that is references by another clearing account"
                    )

                now = datetime.now(tz=timezone.utc)
                revision_id = await conn.fetchval(
                    "insert into account_revision (user_id, account_id, started, committed) "
                    "values ($1, $2, $3, $4) returning id",
                    user.id,
                    account_id,
                    now,
                    now,
                )
                await conn.execute(
                    "insert into account_history (id, revision_id, name, description, priority, deleted) "
                    "select $1, $2, name, description, priority, true "
                    "from account_history ah where ah.id = $1 and ah.revision_id = $3 ",
                    account_id,
                    revision_id,
                    row["revision_id"],
                )

                await create_group_log(
                    conn=conn,
                    group_id=group_id,
                    user=user,
                    type="account-deleted",
                    message=f"deleted account account {row['name']}",
                )

    async def sync_account(
        self, *, conn: asyncpg.Connection, user: User, account: RawAccount
    ) -> tuple[int, int]:
        if account.id > 0:
            await self._update_account(
                conn=conn,
                user=user,
                account_id=account.id,
                name=account.name,
                description=account.description,
                owning_user_id=account.owning_user_id,
                priority=account.priority,
                clearing_shares=account.clearing_shares,
            )
            return account.id, account.id

        if account.type is None:
            raise InvalidCommand("new account must have 'type' set")

        new_acc_id = await self._create_account(
            conn=conn,
            user=user,
            group_id=account.group_id,
            type=account.type,
            name=account.name,
            description=account.description,
            owning_user_id=account.owning_user_id,
            priority=account.priority,
            clearing_shares=account.clearing_shares,
        )
        return account.id, new_acc_id

    async def sync_accounts(
        self, *, user: User, group_id: int, accounts: list[RawAccount]
    ) -> dict[int, int]:
        all_accounts_in_same_group = all([a.group_id == group_id for a in accounts])
        if not all_accounts_in_same_group:
            raise InvalidCommand("all accounts must belong to the same group")

        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                can_write, _ = await check_group_permissions(
                    conn=conn, group_id=group_id, user=user, can_write=True
                )

                if not can_write:
                    raise PermissionError("need write access to group")

                new_account_id_map: dict[int, int] = {}

                for account in filter(
                    lambda acc: acc.type == AccountType.personal, accounts
                ):
                    old_acc_id, new_acc_id = await self.sync_account(
                        conn=conn, user=user, account=account
                    )
                    new_account_id_map[old_acc_id] = new_acc_id

                clearing_accounts = list(
                    filter(lambda acc: acc.type == AccountType.clearing, accounts)
                )
                # TODO: improve this very inefficient implementation
                # first step: use a dict instead of a list
                while len(clearing_accounts) > 0:
                    for account in clearing_accounts[:]:  # copy as we remove items
                        if account.clearing_shares:
                            account.clearing_shares = {
                                new_account_id_map.get(k, k): v
                                for k, v in account.clearing_shares.items()
                            }
                        if account.clearing_shares and all(
                            [x > 0 for x in account.clearing_shares.keys()]
                        ):
                            old_acc_id, new_acc_id = await self.sync_account(
                                conn=conn, user=user, account=account
                            )
                            new_account_id_map[old_acc_id] = new_acc_id
                            clearing_accounts.remove(account)

                return new_account_id_map

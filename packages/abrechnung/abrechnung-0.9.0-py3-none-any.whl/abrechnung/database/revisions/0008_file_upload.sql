-- revision: 156aef63
-- requires: dbcccb58

create or replace function transaction_revision_updated() returns trigger as
$$
<<locals>> declare
    group_id       grp.id%TYPE;
    transaction_id integer;
begin
    select
        t.group_id,
        t.id
    into locals.group_id, locals.transaction_id
    from
        transaction t
    where t.id = (case when NEW is null then OLD.transaction_id else NEW.transaction_id end);

    -- A deletion should only be able to occur for uncommitted revisions
    if NEW is null then
        call notify_user('transaction', OLD.user_id, locals.group_id::bigint,
                         json_build_object('element_id', locals.group_id, 'transaction_id', locals.transaction_id));
    elseif NEW.committed is null then
        call notify_user('transaction', NEW.user_id, locals.group_id::bigint,
                         json_build_object('element_id', locals.group_id, 'transaction_id', locals.transaction_id));
    else
        call notify_group('transaction', locals.group_id, locals.group_id::bigint,
                          json_build_object('element_id', locals.group_id, 'transaction_id', locals.transaction_id));
    end if;

    return null;
end;
$$ language plpgsql;

-- disallow empty strings in certain fields
alter table account_history add constraint name_not_empty check ( name <> '' );
alter table transaction_history add constraint description_not_empty check ( description <> '' );
alter table grp add constraint name_not_empty check ( name <> '' );
alter table purchase_item_history add constraint name_not_empty check ( name <> '' );

drop view current_transaction_state;
drop view committed_transaction_state;
drop view committed_transaction_history;

drop view pending_transaction_revisions;
drop view pending_transaction_history;

drop view pending_purchase_item_full;
drop view pending_purchase_item_history;
drop view committed_purchase_item_state;
drop view committed_purchase_item_history;

drop view latest_account;

drop view purchase_item_usages_as_json;
drop view debitor_shares_as_json;
drop view creditor_shares_as_json;

create table if not exists blob (
    id        serial primary key,
    content   bytea not null,
    mime_type text not null
);

create table if not exists file (
    id             serial primary key,
    transaction_id integer not null references transaction (id) on delete cascade
);

create table if not exists file_history (
    id             integer references file(id) on delete cascade,
    revision_id    bigint not null references transaction_revision (id) on delete cascade,
    primary key (id, revision_id),
    filename       text not null constraint filename_not_empty check (filename <> ''),
    blob_id        integer references blob(id) on delete cascade,
    deleted        bool default false
);

-- notifications for transaction file attachments
create or replace function file_history_updated() returns trigger as
$$
<<locals>> declare
    group_id       grp.id%TYPE;
    transaction_id integer;
begin
    select
        transaction.group_id,
        transaction.id
    into locals.group_id, locals.transaction_id
    from
        transaction
        join file f on transaction.id = f.transaction_id
    where
        f.id = (case when NEW is null then OLD.id else NEW.id end);

    call notify_group('transaction', locals.group_id, locals.group_id::bigint,
                      json_build_object('element_id', locals.group_id, 'transaction_id', locals.transaction_id));
    return null;
end;
$$ language plpgsql;

drop trigger if exists file_history_trig on file_history;
create trigger file_history_trig
    after insert or update or delete
    on file_history
    for each row
execute function file_history_updated();

create or replace view purchase_item_usages_as_json as
    select
        piu.revision_id,
        piu.item_id,
        sum(piu.share_amount)    as n_usages,
        array_agg(piu.account_id) as involved_accounts,
        jsonb_agg(piu.*)         as usages
    from
        purchase_item_usage piu
    group by
        piu.revision_id, piu.item_id;

create or replace view debitor_shares_as_json as
    select
        ds.revision_id,
        ds.transaction_id,
        sum(ds.shares)           as n_shares,
        array_agg(ds.account_id) as involved_accounts,
        jsonb_agg(ds.*)          as shares
    from
        debitor_share ds
    group by
        ds.revision_id, ds.transaction_id;

create or replace view creditor_shares_as_json as
    select
        cs.revision_id,
        cs.transaction_id,
        sum(cs.shares)           as n_shares,
        array_agg(cs.account_id) as involved_accounts,
        jsonb_agg(cs.*)          as shares
    from
        creditor_share cs
    group by
        cs.revision_id, cs.transaction_id;

create or replace view aggregated_committed_file_history as (
select
    sub.revision_id,
    sub.transaction_id,
    sub.file_id,
    sub.user_id,
    sub.started                                          as revision_started,
    sub.committed                                        as revision_committed,
    first_value(sub.filename) over outer_window          as filename,
    first_value(sub.mime_type) over outer_window         as mime_type,
    first_value(sub.blob_id) over outer_window           as blob_id,
    first_value(sub.deleted) over outer_window           as deleted
from (
    select
        tr.id                 as revision_id,
        tr.transaction_id,
        tr.user_id,
        tr.started,
        tr.committed,
        f.id                 as file_id,
        count(f.id) over wnd as id_partition,
        fh.filename,
        blob.mime_type,
        fh.blob_id,
        fh.deleted
    from
        transaction_revision tr
        join file f on tr.transaction_id = f.transaction_id
        left join file_history fh on fh.id = f.id and tr.id = fh.revision_id
        left join blob on blob.id = fh.blob_id
    where
        tr.committed is not null window wnd as (partition by f.id order by committed asc)
) as sub window outer_window as (partition by sub.file_id, sub.id_partition order by sub.revision_id)
);

create or replace view aggregated_pending_file_history as (
select
    tr.id                               as revision_id,
    tr.transaction_id,
    tr.user_id                          as changed_by,
    tr.started                          as revision_started,
    f.id                                as file_id,
    fh.filename,
    blob.mime_type,
    fh.blob_id,
    fh.deleted
from
    transaction_revision tr
    join file f on tr.transaction_id = f.transaction_id
    join file_history fh on fh.id = f.id and tr.id = fh.revision_id
    left join blob on blob.id = fh.blob_id
where
    tr.committed is null
);

create or replace function committed_file_state_valid_at(
    valid_at timestamptz = now()
)
returns table (
    file_id            int,
    revision_id        bigint,
    transaction_id     int,
    changed_by         int,
    revision_started   timestamptz,
    revision_committed timestamptz,
    filename           text,
    mime_type          text,
    blob_id            int,
    deleted            bool
)
as
$$
select distinct on (file_id)
    file_id,
    revision_id,
    transaction_id,
    user_id            as changed_by,
    revision_started,
    revision_committed,
    filename,
    mime_type,
    blob_id,
    deleted
from
    aggregated_committed_file_history
where
    revision_committed <= committed_file_state_valid_at.valid_at
    and filename is not null
order by
    file_id, revision_committed desc
$$ language sql
    security invoker
    stable;

create or replace view aggregated_committed_transaction_position_history as (
    select
        sub.revision_id,
        sub.transaction_id,
        sub.item_id,
        sub.user_id,
        sub.started                                          as revision_started,
        sub.committed                                        as revision_committed,
        first_value(sub.name) over outer_window              as name,
        first_value(sub.price) over outer_window             as price,
        first_value(sub.communist_shares) over outer_window  as communist_shares,
        first_value(sub.deleted) over outer_window           as deleted,
        first_value(sub.n_usages) over outer_window          as n_usages,
        first_value(sub.usages) over outer_window            as usages,
        first_value(sub.involved_accounts) over outer_window as involved_accounts
    from (
        select
            tr.id                 as revision_id,
            tr.transaction_id,
            tr.user_id,
            tr.started,
            tr.committed,
            pi.id                 as item_id,
            count(pi.id) over wnd as id_partition,
            pih.name,
            pih.price,
            pih.communist_shares,
            pih.deleted,
            coalesce(piu.n_usages, 0)           as n_usages,
            coalesce(piu.usages, '[]'::jsonb)   as usages,
            coalesce(piu.involved_accounts, array[]::int[]) as involved_accounts
        from
            transaction_revision tr
            join purchase_item pi on tr.transaction_id = pi.transaction_id
            left join purchase_item_history pih on pih.id = pi.id and tr.id = pih.revision_id
            left join purchase_item_usages_as_json piu on pi.id = piu.item_id and tr.id = piu.revision_id
        where
            tr.committed is not null window wnd as (partition by pi.id order by committed asc)
    ) as sub window outer_window as (partition by sub.item_id, sub.id_partition order by sub.revision_id)
);

create or replace view aggregated_pending_transaction_position_history as (
    select
        tr.id                               as revision_id,
        tr.transaction_id,
        tr.user_id                          as changed_by,
        tr.started                          as revision_started,
        pi.id                               as item_id,
        pih.name,
        pih.price,
        pih.communist_shares,
        pih.deleted,
        coalesce(piu.n_usages, 0)           as n_usages,
        coalesce(piu.usages, '[]'::jsonb)   as usages,
        coalesce(piu.involved_accounts, array[]::int[]) as involved_accounts
    from
        transaction_revision tr
        join purchase_item pi on tr.transaction_id = pi.transaction_id
        join purchase_item_history pih on pih.id = pi.id and tr.id = pih.revision_id
        left join purchase_item_usages_as_json piu on pi.id = piu.item_id and tr.id = piu.revision_id
    where
        tr.committed is null
);

create or replace function committed_transaction_position_state_valid_at(
    valid_at timestamptz = now()
)
returns table (
    item_id            int,
    revision_id        bigint,
    transaction_id     int,
    changed_by         int,
    revision_started   timestamptz,
    revision_committed timestamptz,
    name               text,
    price              double precision,
    communist_shares   double precision,
    deleted            bool,
    n_usages           int,
    usages             jsonb,
    involved_accounts  int[]
)
as
$$
select distinct on (acph.item_id)
    acph.item_id,
    acph.revision_id,
    acph.transaction_id,
    acph.user_id            as changed_by,
    acph.revision_started,
    acph.revision_committed,
    acph.name,
    acph.price,
    acph.communist_shares,
    acph.deleted,
    acph.n_usages,
    acph.usages,
    acph.involved_accounts
from
    aggregated_committed_transaction_position_history acph
where
    acph.revision_committed <= committed_transaction_position_state_valid_at.valid_at
    and acph.name is not null
order by
    acph.item_id, acph.revision_committed desc
$$ language sql
    security invoker
    stable;

create or replace view aggregated_committed_transaction_history as (
    select
        sub.revision_id,
        sub.transaction_id,
        sub.user_id,
        sub.group_id,
        sub.started                                                 as revision_started,
        sub.committed                                               as revision_committed,
        sub.type,
        first_value(sub.value) over outer_window                    as value,
        first_value(sub.description) over outer_window              as description,
        first_value(sub.currency_symbol) over outer_window          as currency_symbol,
        first_value(sub.currency_conversion_rate) over outer_window as currency_conversion_rate,
        first_value(sub.billed_at) over outer_window                as billed_at,
        first_value(sub.deleted) over outer_window                  as deleted,
        first_value(sub.n_creditor_shares) over outer_window        as n_creditor_shares,
        first_value(sub.creditor_shares) over outer_window          as creditor_shares,
        first_value(sub.n_debitor_shares) over outer_window         as n_debitor_shares,
        first_value(sub.debitor_shares) over outer_window           as debitor_shares,
        first_value(sub.involved_accounts) over outer_window        as involved_accounts
    from (
        select
            tr.id                 as revision_id,
            tr.transaction_id,
            tr.user_id,
            tr.started,
            tr.committed,
            t.group_id,
            t.type,
            count(th.id) over wnd as id_partition,
            th.value,
            th.currency_symbol,
            th.currency_conversion_rate,
            th.description,
            th.billed_at,
            th.deleted,
            coalesce(csaj.n_shares, 0)        as n_creditor_shares,
            coalesce(csaj.shares, '[]'::jsonb) as creditor_shares,
            coalesce(dsaj.n_shares, 0)        as n_debitor_shares,
            coalesce(dsaj.shares, '[]'::jsonb) as debitor_shares,
            coalesce(csaj.involved_accounts, array[]::int[]) || coalesce(dsaj.involved_accounts, array[]::int[]) as involved_accounts
        from
            transaction_revision tr
            join transaction t on tr.transaction_id = t.id
            left join transaction_history th on t.id = th.id and tr.id = th.revision_id
            left join creditor_shares_as_json csaj on t.id = csaj.transaction_id and tr.id = csaj.revision_id
            left join debitor_shares_as_json dsaj on t.id = dsaj.transaction_id and tr.id = dsaj.revision_id
        where
            tr.committed is not null window wnd as (partition by tr.transaction_id order by committed asc)
    ) as sub window outer_window as (partition by sub.transaction_id, sub.id_partition order by sub.revision_id)
);

create or replace view aggregated_pending_transaction_history as (
    select
        tr.id                             as revision_id,
        tr.transaction_id,
        tr.user_id                        as changed_by,
        tr.started                        as revision_started,
        t.group_id,
        t.type,
        th.value,
        th.currency_symbol,
        th.currency_conversion_rate,
        th.description,
        th.billed_at,
        th.deleted,
        coalesce(csaj.n_shares, 0)        as n_creditor_shares,
        coalesce(csaj.shares, '[]'::jsonb) as creditor_shares,
        coalesce(dsaj.n_shares, 0)        as n_debitor_shares,
        coalesce(dsaj.shares, '[]'::jsonb) as debitor_shares,
        coalesce(csaj.involved_accounts, array[]::int[]) || coalesce(dsaj.involved_accounts, array[]::int[]) as involved_accounts
    from
        transaction_revision tr
        join transaction t on tr.transaction_id = t.id
        join transaction_history th on t.id = th.id and tr.id = th.revision_id
        left join creditor_shares_as_json csaj on t.id = csaj.transaction_id and tr.id = csaj.revision_id
        left join debitor_shares_as_json dsaj on t.id = dsaj.transaction_id and tr.id = dsaj.revision_id
    where
        tr.committed is null
);

create or replace function committed_transaction_state_valid_at(
    valid_at timestamptz = now()
)
returns table (
    revision_id              bigint,
    transaction_id           int,
    changed_by               int,
    revision_started         timestamptz,
    revision_committed       timestamptz,
    group_id                 int,
    type                     text,
    value                    double precision,
    currency_symbol          text,
    currency_conversion_rate double precision,
    description              text,
    billed_at                date,
    deleted                  bool,
    n_creditor_shares        int,
    creditor_shares          jsonb,
    n_debitor_shares         int,
    debitor_shares           jsonb,
    involved_accounts        int[]
)
as
$$
select distinct on (acth.transaction_id)
    acth.revision_id,
    acth.transaction_id,
    acth.user_id as changed_by,
    acth.revision_started,
    acth.revision_committed,
    acth.group_id,
    acth.type,
    acth.value,
    acth.currency_symbol,
    acth.currency_conversion_rate,
    acth.description,
    acth.billed_at,
    acth.deleted,
    acth.n_creditor_shares,
    acth.creditor_shares,
    acth.n_debitor_shares,
    acth.debitor_shares,
    acth.involved_accounts
from
    aggregated_committed_transaction_history acth
where
    acth.revision_committed <= committed_transaction_state_valid_at.valid_at
    and acth.description is not null
order by
    acth.transaction_id, acth.revision_committed desc
$$ language sql
    security invoker
    stable;

create or replace function full_transaction_state_valid_at(
    seen_by_user int,
    valid_at timestamptz = now()
)
returns table (
    transaction_id      int,
    type                text,
    group_id            int,
    last_changed        timestamptz,
    is_wip              bool,
    committed_details   jsonb,
    pending_details     jsonb,
    committed_positions jsonb,
    pending_positions   jsonb,
    committed_files     jsonb,
    pending_files       jsonb
)
as
$$
select
    t.id as transaction_id,
    t.type,
    t.group_id,
    greatest(committed_details.last_changed, committed_positions.last_changed, committed_files.last_changed) as last_changed,
    exists(
        select 1 from transaction_revision tr
        where tr.transaction_id = t.id and tr.user_id = full_transaction_state_valid_at.seen_by_user and tr.committed is null
    ) as is_wip,
    committed_details.json_state as committed_details,
    pending_details.json_state as pending_details,
    committed_positions.json_state as committed_positions,
    pending_positions.json_state as pending_positions,
    committed_files.json_state as committed_files,
    pending_files.json_state as pending_files
from
    transaction t
left join (
    select
        ctsa.transaction_id,
        jsonb_agg(ctsa) as json_state,
        max(ctsa.revision_committed) as last_changed
    from committed_transaction_state_valid_at(full_transaction_state_valid_at.valid_at) ctsa
    group by ctsa.transaction_id
) committed_details on t.id = committed_details.transaction_id
left join (
    select
        apth.transaction_id,
        jsonb_agg(apth) as json_state
    from aggregated_pending_transaction_history apth
    where apth.changed_by = full_transaction_state_valid_at.seen_by_user
    group by apth.transaction_id
) pending_details on t.id = pending_details.transaction_id
left join (
    select
        ctpsa.transaction_id,
        jsonb_agg(ctpsa) as json_state,
        max(ctpsa.revision_committed) as last_changed
    from committed_transaction_position_state_valid_at(full_transaction_state_valid_at.valid_at) ctpsa
    group by ctpsa.transaction_id
) committed_positions on t.id = committed_positions.transaction_id
left join (
    select
        aptph.transaction_id,
        jsonb_agg(aptph) as json_state
    from aggregated_pending_transaction_position_history aptph
    where aptph.changed_by = full_transaction_state_valid_at.seen_by_user
    group by aptph.transaction_id
) pending_positions on t.id = pending_positions.transaction_id
left join (
    select
        cfsva.transaction_id,
        jsonb_agg(cfsva) as json_state,
        max(cfsva.revision_committed) as last_changed
    from committed_file_state_valid_at(full_transaction_state_valid_at.valid_at) cfsva
    group by cfsva.transaction_id
) committed_files on t.id = committed_files.transaction_id
left join (
    select
        apfh.transaction_id,
        jsonb_agg(apfh) as json_state
    from aggregated_pending_file_history apfh
    where apfh.changed_by = full_transaction_state_valid_at.seen_by_user
    group by apfh.transaction_id
) pending_files on t.id = pending_files.transaction_id
where committed_details.json_state is not null or pending_details.json_state is not null
$$ language sql
    security invoker
    stable;

create or replace view aggregated_committed_account_history as (
    select
        sub.revision_id,
        sub.account_id,
        sub.user_id,
        sub.group_id,
        sub.type,
        sub.started                                    as revision_started,
        sub.committed                                  as revision_committed,
        first_value(sub.description) over outer_window as description,
        first_value(sub.name) over outer_window        as name,
        first_value(sub.priority) over outer_window    as priority,
        first_value(sub.deleted) over outer_window     as deleted
    from (
        select
            ar.id                as revision_id,
            ar.account_id,
            ar.user_id,
            ar.started,
            ar.committed,
            a.group_id,
            a.type,
            count(a.id) over wnd as id_partition,
            ah.name,
            ah.description,
            ah.priority,
            ah.deleted
        from
            account_revision ar
            join account a on a.id = ar.account_id
            left join account_history ah on ah.id = a.id and ar.id = ah.revision_id
        where
            ar.committed is not null window wnd as (partition by a.id order by committed asc)
    ) as sub window outer_window as (partition by sub.account_id, sub.id_partition order by sub.revision_id)
);

create or replace function committed_account_state_valid_at(
    valid_at timestamptz = now()
)
returns table (
    account_id         int,
    revision_id        bigint,
    type               text,
    user_id            int,
    group_id           int,
    revision_started   timestamptz,
    revision_committed timestamptz,
    name               text,
    description        text,
    priority           int,
    deleted            bool
)
as
$$
select distinct on (acah.account_id)
    acah.account_id,
    acah.revision_id,
    acah.type,
    acah.user_id,
    acah.group_id,
    acah.revision_started,
    acah.revision_committed,
    acah.name,
    acah.description,
    acah.priority,
    acah.deleted
from
    aggregated_committed_account_history acah
where
    acah.revision_committed <= committed_account_state_valid_at.valid_at
order by
    acah.account_id, acah.revision_committed desc
$$ language sql
    security invoker
    stable;

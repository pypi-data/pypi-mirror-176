import React, { useEffect, useState } from "react";
import InviteLinkCreate from "../../components/groups/InviteLinkCreate";
import { toast } from "react-toastify";
import { api } from "../../core/api";
import { DateTime } from "luxon";
import {
    Alert,
    Grid,
    IconButton,
    List,
    ListItem,
    ListItemSecondaryAction,
    ListItemText,
    Typography,
} from "@mui/material";
import { Add, ContentCopy, Delete } from "@mui/icons-material";
import { MobilePaper } from "../../components/style/mobile";
import { useTitle } from "../../core/utils";
import { ws } from "../../core/api";
import { useAppSelector, useAppDispatch, selectGroupSlice, selectAuthSlice } from "../../store";
import {
    selectGroupById,
    selectCurrentUserPermissions,
    selectGroupMembers,
    selectGroupInvites,
    selectIsGuestUser,
    selectGroupInviteStatus,
    fetchGroupInvites,
    deleteGroupInvite,
    subscribe,
    unsubscribe,
} from "@abrechnung/redux";
import Loading from "../../components/style/Loading";

interface Props {
    groupId: number;
}

export const GroupInvites: React.FC<Props> = ({ groupId }) => {
    const [showModal, setShowModal] = useState(false);
    const dispatch = useAppDispatch();
    const group = useAppSelector((state) => selectGroupById({ state: selectGroupSlice(state), groupId }));
    const invites = useAppSelector((state) => selectGroupInvites({ state: selectGroupSlice(state), groupId }));
    const members = useAppSelector((state) => selectGroupMembers({ state: selectGroupSlice(state), groupId }));
    const permissions = useAppSelector((state) => selectCurrentUserPermissions({ state: state, groupId }));
    const invitesLoadingStatus = useAppSelector((state) =>
        selectGroupInviteStatus({ state: selectGroupSlice(state), groupId })
    );

    const isGuest = useAppSelector((state) => selectIsGuestUser({ state: selectAuthSlice(state) }));

    useTitle(`${group.name} - Invite Links`);

    useEffect(() => {
        dispatch(fetchGroupInvites({ groupId, api }));
        dispatch(subscribe({ subscription: { type: "group_invite", groupId }, websocket: ws }));
        return () => {
            dispatch(unsubscribe({ subscription: { type: "group_invite", groupId }, websocket: ws }));
        };
    }, [dispatch, groupId]);

    const deleteToken = (id) => {
        dispatch(deleteGroupInvite({ groupId, inviteId: id, api }))
            .unwrap()
            .catch((err) => {
                toast.error(err);
            });
    };

    const getMemberUsername = (memberID) => {
        const member = members.find((member) => member.userID === memberID);
        if (member === undefined) {
            return "unknown";
        }
        return member.username;
    };

    const selectLink = (event) => {
        const node = event.target;
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(node);
        selection.removeAllRanges();
        selection.addRange(range);
    };

    const copyToClipboard = (content) => {
        navigator.clipboard.writeText(content);
        toast.info("Link copied to clipboard!");
    };

    return (
        <MobilePaper>
            <Typography component="h3" variant="h5">
                Active Invite Links
            </Typography>
            {isGuest && (
                <Alert severity="info">
                    You are a guest user on this Abrechnung and therefore not permitted to create group invites.
                </Alert>
            )}
            {invitesLoadingStatus === "loading" ? (
                <Loading />
            ) : (
                <List>
                    {invites.length === 0 ? (
                        <ListItem>
                            <ListItemText primary="No Links" />
                        </ListItem>
                    ) : (
                        invites.map((invite) => (
                            <ListItem key={invite.id}>
                                <ListItemText
                                    primary={
                                        invite.token === null ? (
                                            <span>token hidden, was created by another member</span>
                                        ) : (
                                            <span onClick={selectLink}>
                                                {window.location.origin}/invite/
                                                {invite.token}
                                            </span>
                                        )
                                    }
                                    secondary={
                                        <>
                                            {invite.description}, created by {getMemberUsername(invite.createdBy)},
                                            valid until{" "}
                                            {DateTime.fromISO(invite.validUntil).toLocaleString(DateTime.DATETIME_FULL)}
                                            {invite.singleUse && ", single use"}
                                            {invite.joinAsEditor && ", join as editor"}
                                        </>
                                    }
                                />
                                {permissions.canWrite && (
                                    <ListItemSecondaryAction>
                                        <IconButton
                                            color="primary"
                                            onClick={() =>
                                                copyToClipboard(`${window.location.origin}/invite/${invite.token}`)
                                            }
                                        >
                                            <ContentCopy />
                                        </IconButton>
                                        <IconButton color="error" onClick={() => deleteToken(invite.id)}>
                                            <Delete />
                                        </IconButton>
                                    </ListItemSecondaryAction>
                                )}
                            </ListItem>
                        ))
                    )}
                </List>
            )}
            {permissions.canWrite && !isGuest && (
                <>
                    <Grid container justifyContent="center">
                        <IconButton color="primary" onClick={() => setShowModal(true)}>
                            <Add />
                        </IconButton>
                    </Grid>
                    <InviteLinkCreate show={showModal} onClose={() => setShowModal(false)} group={group} />
                </>
            )}
        </MobilePaper>
    );
};

export default GroupInvites;

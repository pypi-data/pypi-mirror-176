import React, { useEffect, useState } from "react";
import { api } from "../../core/api";
import { toast } from "react-toastify";
import { DateTime } from "luxon";
import {
    Button,
    Divider,
    FormControlLabel,
    List,
    ListItem,
    ListItemText,
    Switch,
    TextField,
    Typography,
} from "@mui/material";
import { MobilePaper } from "../../components/style/mobile";
import { Loading } from "../../components/style/Loading";
import { useTitle } from "../../core/utils";
import { ws } from "../../core/api";
import { selectGroupSlice, useAppDispatch, useAppSelector } from "../../store";
import {
    fetchGroupLog,
    selectGroupById,
    selectGroupLogs,
    selectGroupLogStatus,
    selectGroupMembers,
    subscribe,
    unsubscribe,
} from "@abrechnung/redux";

interface Props {
    groupId: number;
}

export const GroupLog: React.FC<Props> = ({ groupId }) => {
    const dispatch = useAppDispatch();
    const group = useAppSelector((state) => selectGroupById({ state: selectGroupSlice(state), groupId }));
    const members = useAppSelector((state) => selectGroupMembers({ state: selectGroupSlice(state), groupId }));
    const logEntries = useAppSelector((state) => selectGroupLogs({ state: selectGroupSlice(state), groupId }));
    const logLoadingStatus = useAppSelector((state) =>
        selectGroupLogStatus({ state: selectGroupSlice(state), groupId })
    );

    const [showAllLogs, setShowAllLogs] = useState(false);
    const [message, setMessage] = useState("");

    useTitle(`${group.name} - Log`);

    useEffect(() => {
        dispatch(fetchGroupLog({ groupId, api }));
        dispatch(subscribe({ subscription: { type: "group_log", groupId }, websocket: ws }));
        return () => {
            dispatch(unsubscribe({ subscription: { type: "group_log", groupId }, websocket: ws }));
        };
    }, [dispatch, groupId]);

    const sendMessage = () => {
        api.sendGroupMessage(groupId, message)
            .then((result) => {
                console.log("sent message");
                setMessage("");
            })
            .catch((err) => {
                console.log("error on send message", err);
                toast.error(err);
            });
    };

    const getMemberUsername = (member_id) => {
        const member = members.find((member) => member.userID === member_id);
        if (member === undefined) {
            return "unknown";
        }
        return member.username;
    };

    const onKeyUp = (key) => {
        key.preventDefault();
        if (key.keyCode === 13) {
            sendMessage();
        }
    };

    const log = showAllLogs ? logEntries : logEntries.filter((entry) => entry.type === "text-message");

    return (
        <MobilePaper>
            <Typography component="h3" variant="h5">
                Group Log
            </Typography>
            <FormControlLabel
                control={
                    <Switch
                        name="showAllLogs"
                        checked={showAllLogs}
                        color="primary"
                        onChange={(e) => setShowAllLogs(e.target.checked)}
                    />
                }
                label="Show all Logs"
            />
            <TextField
                required
                fullWidth
                name="newMessage"
                placeholder="Write a message to the group ..."
                value={message}
                variant="outlined"
                onKeyUp={onKeyUp}
                multiline
                onChange={(e) => setMessage(e.target.value)}
            />
            <Button type="submit" color="primary" onClick={sendMessage}>
                Send
            </Button>
            <Divider variant="middle" />
            <List>
                {logLoadingStatus === undefined || logLoadingStatus === "loading" ? (
                    <Loading />
                ) : (
                    log.map((logEntry) => (
                        <ListItem key={logEntry.id}>
                            <ListItemText
                                primary={`${logEntry.type} - ${logEntry.message}`}
                                secondary={`by ${getMemberUsername(logEntry.userID)}
                            on ${DateTime.fromISO(logEntry.loggedAt).toLocaleString(DateTime.DATETIME_FULL)}`}
                            />
                        </ListItem>
                    ))
                )}
            </List>
        </MobilePaper>
    );
};

export default GroupLog;

import { selectGroupById } from "@abrechnung/redux";
import React from "react";
import { List } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import { changeActiveGroup, selectGroupSlice, useAppDispatch, useAppSelector } from "../store";
import { api } from "../core/api";

interface Props {
    groupId: number;
}

export const GroupListItem: React.FC<Props> = ({ groupId }) => {
    const navigation = useNavigation();
    const dispatch = useAppDispatch();
    const group = useAppSelector((state) => selectGroupById({ state: selectGroupSlice(state), groupId }));

    if (group === undefined) {
        return null;
    }

    return (
        <List.Item
            key={groupId}
            title={group.name}
            description={group.description}
            onPress={() => {
                dispatch(changeActiveGroup({ api, groupId: group.id }))
                    .unwrap()
                    .then(() => {
                        navigation.navigate("GroupStackNavigator", {
                            screen: "TransactionList",
                            params: { groupId },
                        });
                    });
            }}
        />
    );
};

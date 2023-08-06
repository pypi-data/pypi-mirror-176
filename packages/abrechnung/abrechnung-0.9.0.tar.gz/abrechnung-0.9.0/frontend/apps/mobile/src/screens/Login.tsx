import React, { useState } from "react";
import { StyleSheet, TouchableOpacity, View } from "react-native";
import { RootDrawerScreenProps } from "../navigation/types";
import { Appbar, Button, HelperText, ProgressBar, Text, TextInput, useTheme } from "react-native-paper";
import { notify } from "../notifications";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { useAppDispatch } from "../store";
import { Formik, FormikHelpers } from "formik";
import { login } from "@abrechnung/redux";
import { api, websocket } from "../core/api";
import { z } from "zod";
import { SerializedError } from "@reduxjs/toolkit";
import { toFormikValidationSchema } from "@abrechnung/utils";

const validationSchema = z.object({
    server: z.string({ required_error: "server is required" }).url({ message: "invalid server url" }),
    username: z.string({ required_error: "username is required" }),
    password: z.string({ required_error: "password is required" }),
});
type FormSchema = z.infer<typeof validationSchema>;

export const LoginScreen: React.FC<RootDrawerScreenProps<"Login">> = ({ navigation }) => {
    const theme = useTheme();
    const dispatch = useAppDispatch();

    const [showPassword, setShowPassword] = useState(false);

    const toggleShowPassword = () => {
        setShowPassword((oldVal) => !oldVal);
    };

    const handleSubmit = (values: FormSchema, { setSubmitting }: FormikHelpers<FormSchema>) => {
        api.baseApiUrl = values.server;
        dispatch(
            login({
                username: values.username,
                password: values.password,
                sessionName: "Abrechnung Mobile",
                api,
            })
        )
            .unwrap()
            .then(() => {
                websocket.setUrl(`${values.server.replace("http://", "ws://").replace("https://", "ws://")}/api/v1/ws`);
                setSubmitting(false);
            })
            .catch((err: SerializedError) => {
                console.log("error on login", err);
                if (err.message) {
                    notify({ text: err.message });
                }
                setSubmitting(false);
            });
    };

    return (
        <>
            <Appbar.Header theme={{ colors: { primary: theme.colors.surface } }}>
                <Appbar.Content title="Abrechnung" />
            </Appbar.Header>
            <Formik
                validationSchema={toFormikValidationSchema(validationSchema)}
                validateOnBlur={false}
                validateOnChange={false}
                initialValues={{
                    server: "https://demo.abrechnung.sft.lol",
                    username: "",
                    password: "",
                }}
                onSubmit={handleSubmit}
            >
                {({ values, touched, handleSubmit, handleBlur, isSubmitting, errors, setFieldValue }) => (
                    <View style={styles.container}>
                        <TextInput
                            label="Server"
                            returnKeyType="next"
                            autoCapitalize="none"
                            textContentType="URL"
                            keyboardType="url"
                            value={values.server}
                            onBlur={handleBlur("server")}
                            onChangeText={(val) => setFieldValue("server", val)}
                            error={touched.server && !!errors.server}
                        />
                        <HelperText type="error" visible={touched.server && !!errors.server}>
                            {errors.server}
                        </HelperText>

                        <TextInput
                            label="Username"
                            returnKeyType="next"
                            autoCapitalize="none"
                            textContentType="username"
                            value={values.username}
                            onBlur={handleBlur("username")}
                            onChangeText={(val) => setFieldValue("username", val)}
                            error={touched.username && !!errors.username}
                        />
                        <HelperText type="error" visible={touched.username && !!errors.username}>
                            {errors.username}
                        </HelperText>

                        <TextInput
                            label="Password"
                            returnKeyType="done"
                            textContentType="password"
                            autoCapitalize="none"
                            value={values.password}
                            onBlur={handleBlur("password")}
                            onChangeText={(val) => setFieldValue("password", val)}
                            error={touched.password && !!errors.password}
                            secureTextEntry={!showPassword}
                            right={
                                <TextInput.Icon
                                    name={({ color, size }) => (
                                        <MaterialCommunityIcons
                                            name={showPassword ? "eye-off" : "eye"}
                                            color={color}
                                            size={size}
                                            onPress={toggleShowPassword}
                                        />
                                    )}
                                />
                            }
                        />
                        <HelperText type="error" visible={touched.password && !!errors.password}>
                            {errors.password}
                        </HelperText>

                        {isSubmitting ? <ProgressBar indeterminate={true} /> : null}
                        <Button mode="contained" onPress={handleSubmit}>
                            Login
                        </Button>

                        <View style={styles.row}>
                            <Text>Don’t have an account? </Text>
                            <TouchableOpacity onPress={() => navigation.navigate("Register")}>
                                <Text style={styles.link}>Sign up</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                )}
            </Formik>
        </>
    );
};

const styles = StyleSheet.create({
    container: {
        padding: 8,
    },
    row: {
        flexDirection: "row",
        marginTop: 4,
    },
    link: {
        fontWeight: "bold",
        // color: theme.colors.primary,
    },
});

export default LoginScreen;

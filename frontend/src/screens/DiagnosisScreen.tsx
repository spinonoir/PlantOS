import React, { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    Image,
    TouchableOpacity,
    ScrollView,
    ActivityIndicator,
    Alert,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { useLocalSearchParams, useRouter } from "expo-router";
import { api } from "../api/client";
import { theme } from "../theme";

export default function DiagnosisScreen() {
    const { plantId } = useLocalSearchParams<{ plantId: string }>();
    const router = useRouter();
    const [imageUri, setImageUri] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    const takePhoto = async () => {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== "granted") {
            Alert.alert("Permission needed", "Camera permission is required to take photos.");
            return;
        }

        const result = await ImagePicker.launchCameraAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 0.8,
        });

        if (!result.canceled) {
            setImageUri(result.assets[0].uri);
            setResult(null);
        }
    };

    const pickImage = async () => {
        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 0.8,
        });

        if (!result.canceled) {
            setImageUri(result.assets[0].uri);
            setResult(null);
        }
    };

    const submitDiagnosis = async () => {
        if (!imageUri || !plantId) return;

        setLoading(true);
        try {
            const diagnosis = await api.plants.diagnose(plantId, imageUri);
            setResult(diagnosis);
        } catch (error) {
            Alert.alert("Error", "Failed to diagnose plant. Please try again.");
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>AI Health Check</Text>
                <Text style={styles.subtitle}>Take a photo to diagnose issues</Text>
            </View>

            <View style={styles.imageContainer}>
                {imageUri ? (
                    <Image source={{ uri: imageUri }} style={styles.previewImage} />
                ) : (
                    <View style={styles.placeholder}>
                        <Text style={styles.placeholderText}>No photo selected</Text>
                    </View>
                )}
            </View>

            <View style={styles.controls}>
                <TouchableOpacity style={styles.button} onPress={takePhoto}>
                    <Text style={styles.buttonText}>Take Photo</Text>
                </TouchableOpacity>
                <TouchableOpacity style={[styles.button, styles.secondaryButton]} onPress={pickImage}>
                    <Text style={[styles.buttonText, styles.secondaryButtonText]}>Choose from Gallery</Text>
                </TouchableOpacity>
            </View>

            {imageUri && !result && !loading && (
                <TouchableOpacity style={[styles.button, styles.submitButton]} onPress={submitDiagnosis}>
                    <Text style={styles.buttonText}>Run Diagnosis</Text>
                </TouchableOpacity>
            )}

            {loading && (
                <View style={styles.loadingContainer}>
                    <ActivityIndicator size="large" color={theme.colors.primary} />
                    <Text style={styles.loadingText}>Analyzing plant health...</Text>
                </View>
            )}

            {result && (
                <View style={styles.resultContainer}>
                    <Text style={styles.resultTitle}>Diagnosis Results</Text>

                    <View style={styles.card}>
                        <Text style={styles.label}>Condition:</Text>
                        <Text style={styles.value}>{result.diagnosis}</Text>
                    </View>

                    <View style={styles.card}>
                        <Text style={styles.label}>Severity:</Text>
                        <Text style={[
                            styles.value,
                            { color: result.severity === 'high' ? theme.colors.error : theme.colors.text }
                        ]}>
                            {result.severity?.toUpperCase()}
                        </Text>
                    </View>

                    <View style={styles.card}>
                        <Text style={styles.label}>Recommendations:</Text>
                        {result.recommendations?.map((rec: string, index: number) => (
                            <Text key={index} style={styles.bulletPoint}>• {rec}</Text>
                        ))}
                    </View>

                    <TouchableOpacity
                        style={[styles.button, styles.doneButton]}
                        onPress={() => router.back()}
                    >
                        <Text style={styles.buttonText}>Done</Text>
                    </TouchableOpacity>
                </View>
            )}
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
        padding: 20,
    },
    header: {
        marginBottom: 20,
    },
    title: {
        fontSize: 24,
        fontWeight: "bold",
        color: theme.colors.text,
    },
    subtitle: {
        fontSize: 16,
        color: theme.colors.textSecondary,
        marginTop: 5,
    },
    imageContainer: {
        alignItems: "center",
        marginBottom: 20,
    },
    previewImage: {
        width: "100%",
        height: 300,
        borderRadius: 12,
        resizeMode: "cover",
    },
    placeholder: {
        width: "100%",
        height: 300,
        borderRadius: 12,
        backgroundColor: theme.colors.surface,
        justifyContent: "center",
        alignItems: "center",
        borderWidth: 2,
        borderColor: theme.colors.border,
        borderStyle: "dashed",
    },
    placeholderText: {
        color: theme.colors.textSecondary,
    },
    controls: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginBottom: 20,
    },
    button: {
        backgroundColor: theme.colors.primary,
        paddingVertical: 12,
        paddingHorizontal: 20,
        borderRadius: 8,
        alignItems: "center",
        flex: 1,
        marginHorizontal: 5,
    },
    buttonText: {
        color: "#fff",
        fontWeight: "600",
        fontSize: 16,
    },
    secondaryButton: {
        backgroundColor: "transparent",
        borderWidth: 1,
        borderColor: theme.colors.primary,
    },
    secondaryButtonText: {
        color: theme.colors.primary,
    },
    submitButton: {
        backgroundColor: theme.colors.secondary,
        marginBottom: 20,
    },
    loadingContainer: {
        alignItems: "center",
        marginVertical: 20,
    },
    loadingText: {
        marginTop: 10,
        color: theme.colors.textSecondary,
    },
    resultContainer: {
        marginTop: 20,
        paddingBottom: 40,
    },
    resultTitle: {
        fontSize: 20,
        fontWeight: "bold",
        marginBottom: 15,
        color: theme.colors.text,
    },
    card: {
        backgroundColor: theme.colors.surface,
        padding: 15,
        borderRadius: 8,
        marginBottom: 10,
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.1,
        shadowRadius: 2,
        elevation: 2,
    },
    label: {
        fontSize: 14,
        color: theme.colors.textSecondary,
        marginBottom: 5,
    },
    value: {
        fontSize: 18,
        fontWeight: "600",
        color: theme.colors.text,
    },
    bulletPoint: {
        fontSize: 16,
        color: theme.colors.text,
        marginLeft: 10,
        marginBottom: 5,
    },
    doneButton: {
        marginTop: 20,
    },
});

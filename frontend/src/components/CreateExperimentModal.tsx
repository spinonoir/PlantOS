import React, { useState } from "react";
import {
    Modal,
    View,
    Text,
    TextInput,
    TouchableOpacity,
    StyleSheet,
    ScrollView,
    Alert,
} from "react-native";
import { theme } from "../theme";

interface Props {
    visible: boolean;
    onClose: () => void;
    onSubmit: (data: {
        hypothesis: string;
        metric_name: string;
        variants: { name: string; description: string }[];
    }) => void;
}

export default function CreateExperimentModal({ visible, onClose, onSubmit }: Props) {
    const [hypothesis, setHypothesis] = useState("");
    const [metricName, setMetricName] = useState("");
    const [variants, setVariants] = useState<{ name: string; description: string }[]>([
        { name: "", description: "" },
        { name: "", description: "" },
    ]);

    const handleAddVariant = () => {
        setVariants([...variants, { name: "", description: "" }]);
    };

    const handleRemoveVariant = (index: number) => {
        if (variants.length <= 2) {
            Alert.alert("Minimum Variants", "You need at least 2 variants for an experiment.");
            return;
        }
        setVariants(variants.filter((_, i) => i !== index));
    };

    const handleVariantChange = (index: number, field: "name" | "description", value: string) => {
        const updated = [...variants];
        updated[index][field] = value;
        setVariants(updated);
    };

    const handleSubmit = () => {
        if (!hypothesis.trim()) {
            Alert.alert("Missing Hypothesis", "Please enter a hypothesis.");
            return;
        }
        if (!metricName.trim()) {
            Alert.alert("Missing Metric", "Please enter a metric name.");
            return;
        }
        if (variants.some((v) => !v.name.trim())) {
            Alert.alert("Missing Variant Names", "All variants must have names.");
            return;
        }

        onSubmit({ hypothesis, metric_name: metricName, variants });

        // Reset form
        setHypothesis("");
        setMetricName("");
        setVariants([
            { name: "", description: "" },
            { name: "", description: "" },
        ]);
    };

    return (
        <Modal visible={visible} animationType="slide" transparent>
            <View style={styles.overlay}>
                <View style={styles.container}>
                    <View style={styles.header}>
                        <Text style={styles.title}>New Experiment</Text>
                        <TouchableOpacity onPress={onClose}>
                            <Text style={styles.closeButton}>×</Text>
                        </TouchableOpacity>
                    </View>

                    <ScrollView style={styles.content}>
                        <Text style={styles.label}>Hypothesis</Text>
                        <TextInput
                            style={styles.input}
                            placeholder="e.g., More light leads to faster growth"
                            value={hypothesis}
                            onChangeText={setHypothesis}
                            multiline
                        />

                        <Text style={styles.label}>Metric Name</Text>
                        <TextInput
                            style={styles.input}
                            placeholder="e.g., growth_rate, leaf_count"
                            value={metricName}
                            onChangeText={setMetricName}
                        />

                        <View style={styles.sectionHeader}>
                            <Text style={styles.label}>Variants</Text>
                            <TouchableOpacity onPress={handleAddVariant}>
                                <Text style={styles.addButton}>+ Add Variant</Text>
                            </TouchableOpacity>
                        </View>

                        {variants.map((variant, index) => (
                            <View key={index} style={styles.variantCard}>
                                <View style={styles.variantHeader}>
                                    <Text style={styles.variantLabel}>Variant {index + 1}</Text>
                                    {variants.length > 2 && (
                                        <TouchableOpacity onPress={() => handleRemoveVariant(index)}>
                                            <Text style={styles.removeButton}>Remove</Text>
                                        </TouchableOpacity>
                                    )}
                                </View>
                                <TextInput
                                    style={styles.input}
                                    placeholder="Variant name"
                                    value={variant.name}
                                    onChangeText={(text) => handleVariantChange(index, "name", text)}
                                />
                                <TextInput
                                    style={styles.input}
                                    placeholder="Description (optional)"
                                    value={variant.description}
                                    onChangeText={(text) => handleVariantChange(index, "description", text)}
                                    multiline
                                />
                            </View>
                        ))}
                    </ScrollView>

                    <View style={styles.footer}>
                        <TouchableOpacity style={styles.cancelButton} onPress={onClose}>
                            <Text style={styles.cancelButtonText}>Cancel</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
                            <Text style={styles.submitButtonText}>Create</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        </Modal>
    );
}

const styles = StyleSheet.create({
    overlay: {
        flex: 1,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        justifyContent: "center",
        alignItems: "center",
    },
    container: {
        backgroundColor: theme.colors.background,
        borderRadius: 12,
        width: "90%",
        maxHeight: "80%",
        overflow: "hidden",
    },
    header: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        padding: 20,
        borderBottomWidth: 1,
        borderBottomColor: theme.colors.border,
    },
    title: {
        fontSize: 20,
        fontWeight: "bold",
        color: theme.colors.text,
    },
    closeButton: {
        fontSize: 32,
        color: theme.colors.textSecondary,
        lineHeight: 32,
    },
    content: {
        padding: 20,
    },
    label: {
        fontSize: 16,
        fontWeight: "600",
        color: theme.colors.text,
        marginBottom: 8,
        marginTop: 12,
    },
    input: {
        borderWidth: 1,
        borderColor: theme.colors.border,
        borderRadius: 8,
        padding: 12,
        fontSize: 16,
        color: theme.colors.text,
        backgroundColor: theme.colors.background,
    },
    sectionHeader: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginTop: 12,
    },
    addButton: {
        color: theme.colors.primary,
        fontSize: 14,
        fontWeight: "600",
    },
    variantCard: {
        backgroundColor: theme.colors.surface,
        padding: 12,
        borderRadius: 8,
        marginTop: 12,
    },
    variantHeader: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 8,
    },
    variantLabel: {
        fontSize: 14,
        fontWeight: "600",
        color: theme.colors.text,
    },
    removeButton: {
        color: theme.colors.error,
        fontSize: 14,
    },
    footer: {
        flexDirection: "row",
        padding: 20,
        borderTopWidth: 1,
        borderTopColor: theme.colors.border,
        gap: 12,
    },
    cancelButton: {
        flex: 1,
        padding: 12,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: theme.colors.border,
        alignItems: "center",
    },
    cancelButtonText: {
        color: theme.colors.text,
        fontSize: 16,
        fontWeight: "600",
    },
    submitButton: {
        flex: 1,
        padding: 12,
        borderRadius: 8,
        backgroundColor: theme.colors.primary,
        alignItems: "center",
    },
    submitButtonText: {
        color: "#fff",
        fontSize: 16,
        fontWeight: "600",
    },
});

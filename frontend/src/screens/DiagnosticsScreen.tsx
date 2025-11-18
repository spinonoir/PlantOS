import { useState } from "react";
import { Button, ScrollView, StyleSheet, Text, TextInput } from "react-native";

import { api } from "@/api/client";

export function DiagnosticsScreen() {
  const [description, setDescription] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await api.ai.health({ description });
      setResult(
        `${response.diagnosis} • ${response.recommendations.join(", ")}`,
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Health Check</Text>
      <TextInput
        style={styles.input}
        multiline
        placeholder="Describe what you observe"
        value={description}
        onChangeText={setDescription}
      />
      <Button
        title={loading ? "Analyzing…" : "Run diagnosis"}
        onPress={handleSubmit}
        disabled={loading}
      />
      {result && <Text style={styles.result}>{result}</Text>}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    gap: 12,
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
  },
  input: {
    minHeight: 120,
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 12,
    padding: 12,
    textAlignVertical: "top",
  },
  result: {
    marginTop: 16,
    fontSize: 16,
    color: "#065F46",
  },
});

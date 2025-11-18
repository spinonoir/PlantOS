import { useEffect, useState } from "react";
import { FlatList, StyleSheet, Text, View } from "react-native";

import { api } from "@/api/client";

export function ExperimentsScreen() {
  const [experiments, setExperiments] = useState<any[]>([]);

  useEffect(() => {
    api.experiments
      .list()
      .then(setExperiments)
      .catch(() => setExperiments([]));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Experiment Studio</Text>
      <FlatList
        data={experiments}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>{item.name}</Text>
            <Text style={styles.cardSubtitle}>{item.hypothesis}</Text>
            <Text style={styles.metric}>{item.metric_keys?.join(", ")}</Text>
          </View>
        )}
        ListEmptyComponent={
          <Text style={styles.empty}>
            Create variants from the backend dashboard to see them here.
          </Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
    marginBottom: 12,
  },
  card: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: "#fff",
    marginBottom: 12,
    gap: 4,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "600",
  },
  cardSubtitle: {
    fontSize: 14,
    color: "#6B7280",
  },
  metric: {
    fontSize: 12,
    color: "#10B981",
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 32,
  },
});

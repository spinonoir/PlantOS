import { useEffect, useState } from "react";
import {
  FlatList,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from "react-native";

import { api } from "@/api/client";
import { Experiment } from "@/types/plants";
import CreateExperimentModal from "@/components/CreateExperimentModal";
import { theme } from "@/theme";

export function ExperimentsScreen() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [simulatingId, setSimulatingId] = useState<string | null>(null);

  const loadExperiments = () => {
    setLoading(true);
    api.experiments
      .list()
      .then((data) => setExperiments(data as Experiment[]))
      .catch(() => setExperiments([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadExperiments();
  }, []);

  const handleCreateExperiment = async (data: {
    hypothesis: string;
    metric_name: string;
    variants: { name: string; description: string }[];
  }) => {
    try {
      await api.experiments.create(data);
      setModalVisible(false);
      loadExperiments();
      Alert.alert("Success", "Experiment created successfully!");
    } catch (error) {
      Alert.alert("Error", "Failed to create experiment.");
      console.error(error);
    }
  };

  const handleSimulate = async (experimentId: string) => {
    setSimulatingId(experimentId);
    try {
      await api.experiments.simulate(experimentId);
      loadExperiments();
      Alert.alert("Success", "Simulation completed!");
    } catch (error) {
      Alert.alert("Error", "Failed to run simulation.");
      console.error(error);
    } finally {
      setSimulatingId(null);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Experiment Studio</Text>
        <TouchableOpacity
          style={styles.createButton}
          onPress={() => setModalVisible(true)}
        >
          <Text style={styles.createButtonText}>+ New</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color={theme.colors.primary} style={styles.loader} />
      ) : (
        <FlatList
          data={experiments}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardTitle}>{item.hypothesis}</Text>
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>{item.status}</Text>
                </View>
              </View>

              <Text style={styles.metricLabel}>
                Metric: <Text style={styles.metricValue}>{item.metric_name}</Text>
              </Text>

              <View style={styles.variantsContainer}>
                <Text style={styles.variantsTitle}>Variants:</Text>
                {item.variants.map((variant) => (
                  <View key={variant.id} style={styles.variantRow}>
                    <View style={styles.variantInfo}>
                      <Text style={styles.variantName}>{variant.name}</Text>
                      {variant.description && (
                        <Text style={styles.variantDesc}>{variant.description}</Text>
                      )}
                    </View>
                    <View style={styles.metricContainer}>
                      <Text style={styles.metricScore}>
                        {variant.metric.toFixed(2)}
                      </Text>
                    </View>
                  </View>
                ))}
              </View>

              <TouchableOpacity
                style={[
                  styles.simulateButton,
                  simulatingId === item.id && styles.simulateButtonDisabled,
                ]}
                onPress={() => handleSimulate(item.id)}
                disabled={simulatingId === item.id}
              >
                {simulatingId === item.id ? (
                  <ActivityIndicator size="small" color="#fff" />
                ) : (
                  <Text style={styles.simulateButtonText}>Run Simulation</Text>
                )}
              </TouchableOpacity>
            </View>
          )}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No experiments yet</Text>
              <Text style={styles.emptySubtext}>
                Create your first experiment to get started
              </Text>
            </View>
          }
        />
      )}

      <CreateExperimentModal
        visible={modalVisible}
        onClose={() => setModalVisible(false)}
        onSubmit={handleCreateExperiment}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
    color: theme.colors.text,
  },
  createButton: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  createButtonText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 16,
  },
  loader: {
    marginTop: 40,
  },
  card: {
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 8,
    borderRadius: 12,
    backgroundColor: theme.colors.surface,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 12,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: theme.colors.text,
    flex: 1,
    marginRight: 8,
  },
  badge: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  badgeText: {
    color: "#fff",
    fontSize: 12,
    fontWeight: "600",
  },
  metricLabel: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    marginBottom: 12,
  },
  metricValue: {
    fontWeight: "600",
    color: theme.colors.text,
  },
  variantsContainer: {
    marginTop: 8,
    marginBottom: 12,
  },
  variantsTitle: {
    fontSize: 14,
    fontWeight: "600",
    color: theme.colors.text,
    marginBottom: 8,
  },
  variantRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: theme.colors.background,
    borderRadius: 8,
    marginBottom: 6,
  },
  variantInfo: {
    flex: 1,
  },
  variantName: {
    fontSize: 14,
    fontWeight: "600",
    color: theme.colors.text,
  },
  variantDesc: {
    fontSize: 12,
    color: theme.colors.textSecondary,
    marginTop: 2,
  },
  metricContainer: {
    backgroundColor: theme.colors.secondary,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  metricScore: {
    fontSize: 16,
    fontWeight: "600",
    color: "#fff",
  },
  simulateButton: {
    backgroundColor: theme.colors.secondary,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 8,
  },
  simulateButtonDisabled: {
    opacity: 0.6,
  },
  simulateButtonText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 16,
  },
  emptyContainer: {
    alignItems: "center",
    marginTop: 60,
    paddingHorizontal: 40,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: "600",
    color: theme.colors.text,
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    textAlign: "center",
  },
});

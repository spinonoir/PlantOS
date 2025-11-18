import { memo } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import type { Plant } from "@/types/plants";

interface Props {
  plant: Plant;
  onPress?: () => void;
}

function PlantCardBase({ plant, onPress }: Props) {
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [styles.card, pressed && styles.cardPressed]}
    >
      <View style={styles.header}>
        <Text style={styles.title}>{plant.name}</Text>
        <Text style={styles.species}>{plant.species ?? "Unidentified"}</Text>
      </View>
      <View style={styles.row}>
        <Text style={styles.label}>Light:</Text>
        <Text style={styles.value}>{plant.light_level}</Text>
      </View>
      <View style={styles.row}>
        <Text style={styles.label}>Water every</Text>
        <Text style={styles.value}>{plant.watering_interval_days}d</Text>
      </View>
    </Pressable>
  );
}

export const PlantCard = memo(PlantCardBase);

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 3 },
  },
  cardPressed: {
    opacity: 0.8,
  },
  header: {
    marginBottom: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: "600",
  },
  species: {
    fontSize: 14,
    color: "#6B7280",
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 4,
  },
  label: {
    fontSize: 14,
    color: "#4B5563",
  },
  value: {
    fontSize: 14,
    fontWeight: "500",
  },
});

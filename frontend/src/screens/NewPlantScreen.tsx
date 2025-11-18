import { useState } from "react";
import {
  Alert,
  Button,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
} from "react-native";

import { usePlantsStore } from "@/store/plantStore";

export function NewPlantScreen({ navigation }: any) {
  const { addPlant } = usePlantsStore();
  const [name, setName] = useState("");
  const [species, setSpecies] = useState("");
  const [wateringInterval, setWateringInterval] = useState("7");

  const handleSave = async () => {
    if (!name.trim()) {
      Alert.alert("Name is required");
      return;
    }
    await addPlant({
      name,
      species,
      watering_interval_days: Number(wateringInterval) || 7,
    });
    navigation.goBack();
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.label}>Name</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
        placeholder="Fiddle Leaf Fig"
      />

      <Text style={styles.label}>Species</Text>
      <TextInput
        style={styles.input}
        value={species}
        onChangeText={setSpecies}
        placeholder="Ficus lyrata"
      />

      <Text style={styles.label}>Water every (days)</Text>
      <TextInput
        keyboardType="number-pad"
        style={styles.input}
        value={wateringInterval}
        onChangeText={setWateringInterval}
      />

      <Button title="Save" onPress={handleSave} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    gap: 12,
  },
  label: {
    fontSize: 14,
    color: "#374151",
  },
  input: {
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 8,
    padding: 12,
  },
});

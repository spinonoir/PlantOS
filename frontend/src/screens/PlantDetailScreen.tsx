import { useEffect, useState } from "react";
import {
  Button,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";

import { api } from "@/api/client";
import { usePlantsStore } from "@/store/plantStore";
import type { CareTask, TimelineEvent } from "@/types/plants";
import { scheduleReminder } from "@/hooks/useNotifications";

interface Props {
  route: { params: { plantId: string } };
}

export function PlantDetailScreen({ route }: Props) {
  const { plantId } = route.params;
  const plant = usePlantsStore((state) =>
    state.plants.find((item) => item.id === plantId),
  );
  const logEvent = usePlantsStore((state) => state.logEvent);
  const [tasks, setTasks] = useState<CareTask[]>([]);
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [note, setNote] = useState("");

  useEffect(() => {
    api.plants.tasks(plantId).then((data) => setTasks(data as CareTask[]));
    api.plants.timeline(plantId).then((data) => setTimeline(data as TimelineEvent[]));
  }, [plantId]);

  if (!plant) {
    return (
      <View style={styles.center}>
        <Text>Plant not found</Text>
      </View>
    );
  }

  const handleLog = async () => {
    await logEvent(plantId, note);
    setNote("");
    const updated = await api.plants.timeline(plantId);
    setTimeline(updated as TimelineEvent[]);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>{plant.name}</Text>
      <Text style={styles.subtitle}>
        {plant.species ?? "Unidentified species"}
      </Text>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Care Tasks</Text>
        {tasks.map((task) => (
          <View key={task.id} style={styles.row}>
            <View>
              <Text style={styles.label}>{task.signal}</Text>
              <Text style={styles.value}>
                {new Date(task.next_due_at).toLocaleString()}
              </Text>
            </View>
            <Button
              title="Complete"
              onPress={async () => {
                await api.plants.completeTask(task.id);
                const [updatedTasks, updatedTimeline] = await Promise.all([
                  api.plants.tasks(plantId) as Promise<CareTask[]>,
                  api.plants.timeline(plantId) as Promise<TimelineEvent[]>,
                ]);
                setTasks(updatedTasks);
                setTimeline(updatedTimeline);

                // Schedule reminder for next due date
                // Find the updated task
                const updatedTask = updatedTasks.find((t) => t.signal === task.signal);
                if (updatedTask) {
                  // Calculate seconds until due (simplified for demo)
                  const due = new Date(updatedTask.next_due_at).getTime();
                  const now = Date.now();
                  const seconds = Math.max(5, Math.floor((due - now) / 1000));

                  scheduleReminder(`Time to ${updatedTask.signal} ${plant.name}`, "Check your plant!", seconds);
                }
              }}
            />
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Timeline</Text>
        {timeline.map((event) => (
          <View key={event.id} style={styles.row}>
            <Text style={styles.label}>{event.event_type}</Text>
            <Text style={styles.value}>{event.note}</Text>
          </View>
        ))}
        <TextInput
          placeholder="Log observation"
          value={note}
          onChangeText={setNote}
          style={styles.input}
        />
        <Button title="Save note" onPress={handleLog} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    gap: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
  },
  subtitle: {
    fontSize: 16,
    color: "#6B7280",
  },
  section: {
    backgroundColor: "#fff",
    padding: 16,
    borderRadius: 12,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 3 },
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 8,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 8,
  },
  label: {
    fontSize: 14,
    color: "#374151",
  },
  value: {
    fontSize: 14,
    fontWeight: "500",
  },
  input: {
    borderWidth: 1,
    borderColor: "#E5E7EB",
    borderRadius: 8,
    padding: 10,
    marginTop: 8,
    marginBottom: 8,
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});

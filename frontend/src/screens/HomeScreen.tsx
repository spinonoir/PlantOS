import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { useCallback, useEffect } from "react";
import { FlatList, RefreshControl, StyleSheet, Text, View } from "react-native";

import { PlantCard } from "@/components/PlantCard";
import { usePlantsStore } from "@/store/plantStore";
import type { RootStackParamList } from "@/types/navigation";
import type { Plant } from "@/types/plants";

export function HomeScreen() {
  const { plants, hydrate, loading } = usePlantsStore();
  const navigation =
    useNavigation<NativeStackNavigationProp<RootStackParamList>>();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  const renderItem = useCallback(
    ({ item }: { item: Plant }) => (
      <PlantCard
        plant={item}
        onPress={() => navigation.navigate("PlantDetail", { plantId: item.id })}
      />
    ),
    [navigation],
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Your Plants</Text>
        <Text style={styles.subtitle}>Synced locally with care schedules</Text>
      </View>
      <FlatList
        data={plants}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        refreshControl={
          <RefreshControl refreshing={loading} onRefresh={hydrate} />
        }
        ListEmptyComponent={
          <Text style={styles.empty}>
            Add your first plant to begin tracking.
          </Text>
        }
        contentContainerStyle={
          plants.length === 0 ? styles.emptyState : styles.list
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
  header: {
    marginBottom: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
  },
  subtitle: {
    fontSize: 14,
    color: "#6B7280",
  },
  list: {
    paddingBottom: 32,
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 32,
  },
  emptyState: {
    flexGrow: 1,
    justifyContent: "center",
  },
});

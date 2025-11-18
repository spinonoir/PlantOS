import { useEffect, useState } from "react";
import { FlatList, StyleSheet, Text, View } from "react-native";

import { api } from "@/api/client";

export function MarketplaceScreen() {
  const [listings, setListings] = useState<any[]>([]);

  useEffect(() => {
    api.marketplace
      .listings()
      .then(setListings)
      .catch(() => setListings([]));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Marketplace</Text>
      <FlatList
        data={listings}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>{item.title}</Text>
            <Text style={styles.price}>
              {item.currency} {item.price}
            </Text>
            <Text style={styles.meta}>{item.status}</Text>
          </View>
        )}
        ListEmptyComponent={
          <Text style={styles.empty}>
            Mark propagation batches as sale-ready to publish listings.
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
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "600",
  },
  price: {
    fontSize: 14,
    color: "#065F46",
  },
  meta: {
    fontSize: 12,
    color: "#6B7280",
  },
  empty: {
    textAlign: "center",
    color: "#6B7280",
    marginTop: 32,
  },
});

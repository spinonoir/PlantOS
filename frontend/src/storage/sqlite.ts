import { openDatabaseSync } from "expo-sqlite/next";

import type { Plant } from "@/types/plants";

const db = openDatabaseSync("plantos.db");

db.execSync(`
  CREATE TABLE IF NOT EXISTS plants (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT,
    species TEXT,
    light_level TEXT,
    watering_interval_days INTEGER,
    feeding_interval_days INTEGER,
    reminders_enabled INTEGER,
    notes TEXT,
    tags TEXT
  );
`);

type PlantRecord = Omit<Plant, "tags"> & { tags: string };

const serialize = (plant: Plant): PlantRecord => ({
  ...plant,
  tags: JSON.stringify(plant.tags ?? []),
});

const deserialize = (record: PlantRecord): Plant => ({
  ...record,
  tags: JSON.parse(record.tags ?? "[]"),
});

export const PlantStore = {
  save(plants: Plant[]) {
    const statement = db.prepareSync(
      `INSERT OR REPLACE INTO plants (id, name, species, light_level, watering_interval_days, feeding_interval_days, reminders_enabled, notes, tags)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);`,
    );
    plants.forEach((plant) => {
      const row = serialize(plant);
      statement.executeSync([
        row.id,
        row.name,
        row.species ?? null,
        row.light_level,
        row.watering_interval_days,
        row.feeding_interval_days,
        row.reminders_enabled ? 1 : 0,
        row.notes ?? null,
        row.tags,
      ]);
    });
    statement.finalizeSync();
  },
  list(): Plant[] {
    const rows = db.getAllSync<PlantRecord>(
      `SELECT * FROM plants ORDER BY name ASC;`,
    );
    return rows.map(deserialize);
  },
  clear() {
    db.execSync("DELETE FROM plants;");
  },
};

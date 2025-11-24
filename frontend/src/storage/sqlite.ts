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
    tags TEXT,
    created_at TEXT,
    updated_at TEXT
  );

  CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY NOT NULL,
    plant_id TEXT,
    signal TEXT,
    cadence_days INTEGER,
    next_due_at TEXT,
    priority TEXT,
    duration_minutes INTEGER,
    created_at TEXT,
    updated_at TEXT
  );

  CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY NOT NULL,
    plant_id TEXT,
    event_type TEXT,
    note TEXT,
    photo_url TEXT,
    created_at TEXT,
    updated_at TEXT
  );
`);

type PlantRecord = Omit<Plant, "tags"> & { tags: string; created_at?: string; updated_at?: string };

const serialize = (plant: Plant): PlantRecord => ({
  ...plant,
  tags: JSON.stringify(plant.tags ?? []),
  created_at: plant.created_at,
  updated_at: plant.updated_at,
});

const deserialize = (record: PlantRecord): Plant => ({
  ...record,
  tags: JSON.parse(record.tags ?? "[]"),
  created_at: record.created_at,
  updated_at: record.updated_at,
});

export const PlantStore = {
  save(plants: Plant[]) {
    const statement = db.prepareSync(
      `INSERT OR REPLACE INTO plants (id, name, species, light_level, watering_interval_days, feeding_interval_days, reminders_enabled, notes, tags, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);`,
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
        row.created_at ?? new Date().toISOString(),
        row.updated_at ?? new Date().toISOString(),
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

export const TaskStore = {
  save(tasks: any[]) {
    const statement = db.prepareSync(
      `INSERT OR REPLACE INTO tasks (id, plant_id, signal, cadence_days, next_due_at, priority, duration_minutes, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);`,
    );
    tasks.forEach((task) => {
      statement.executeSync([
        task.id,
        task.plant_id,
        task.signal,
        task.cadence_days,
        task.next_due_at,
        task.priority,
        task.duration_minutes,
        task.created_at ?? new Date().toISOString(),
        task.updated_at ?? new Date().toISOString(),
      ]);
    });
    statement.finalizeSync();
  },
  list(): any[] {
    return db.getAllSync(`SELECT * FROM tasks ORDER BY next_due_at ASC;`);
  },
  clear() {
    db.execSync("DELETE FROM tasks;");
  },
};

export const EventStore = {
  save(events: any[]) {
    const statement = db.prepareSync(
      `INSERT OR REPLACE INTO events (id, plant_id, event_type, note, photo_url, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?);`,
    );
    events.forEach((event) => {
      statement.executeSync([
        event.id,
        event.plant_id,
        event.event_type,
        event.note,
        event.photo_url,
        event.created_at ?? new Date().toISOString(),
        event.updated_at ?? new Date().toISOString(),
      ]);
    });
    statement.finalizeSync();
  },
  list(plantId: string): any[] {
    return db.getAllSync(`SELECT * FROM events WHERE plant_id = ? ORDER BY created_at DESC;`, [plantId]);
  },
  clear() {
    db.execSync("DELETE FROM events;");
  },
};

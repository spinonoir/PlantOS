import { create } from "zustand";

import { api } from "@/api/client";
import { PlantStore } from "@/storage/sqlite";
import { SyncAdapter } from "@/storage/sync";
import type { Plant, ScheduleDay, TimelineEvent } from "@/types/plants";

export type PlantForm = {
  name: string;
  species?: string;
  light_level?: Plant["light_level"];
  watering_interval_days?: number;
  feeding_interval_days?: number;
  reminders_enabled?: boolean;
  notes?: string;
  tags?: string[];
};

type PlantState = {
  plants: Plant[];
  schedule: ScheduleDay[];
  timeline: Record<string, TimelineEvent[]>;
  loading: boolean;
  hydrate: () => Promise<void>;
  addPlant: (form: PlantForm) => Promise<void>;
  refreshSchedule: () => Promise<void>;
  logEvent: (plantId: string, note: string) => Promise<void>;
};

export const usePlantsStore = create<PlantState>((set, get) => ({
  plants: [],
  schedule: [],
  timeline: {},
  loading: true,
  hydrate: async () => {
    try {
      set({ loading: true });
      // 1. Try to sync with backend
      await SyncAdapter.pull();

      // 2. Load from local DB (source of truth for UI)
      const plants = PlantStore.list();
      // For schedule, we might need a local calculation or just fetch from API if online
      // For now, let's try to fetch schedule from API, fallback to empty or local calc
      let schedule: ScheduleDay[] = [];
      try {
        schedule = await api.schedules.merged();
      } catch (e) {
        console.log("Offline: could not fetch schedule");
      }

      set({ plants, schedule, loading: false });
    } catch (error) {
      console.error("Hydration failed", error);
      // Fallback to local
      const plants = PlantStore.list();
      set({ plants, loading: false });
    }
  },
  addPlant: async (form: PlantForm) => {
    const payload = {
      light_level: "medium",
      watering_interval_days: 7,
      feeding_interval_days: 30,
      reminders_enabled: true,
      tags: [],
      ...form,
    };
    const plant = await api.plants.create(payload);
    const plants = [...get().plants, plant];
    PlantStore.save(plants);
    set({ plants });
    await get().refreshSchedule();
  },
  refreshSchedule: async () => {
    const schedule = await api.schedules.merged();
    set({ schedule });
  },
  logEvent: async (plantId: string, note: string) => {
    const event = await api.plants.addTimeline(plantId, {
      event_type: "note",
      note,
    });
    set((state) => ({
      timeline: {
        ...state.timeline,
        [plantId]: [...(state.timeline[plantId] ?? []), event],
      },
    }));
  },
}));

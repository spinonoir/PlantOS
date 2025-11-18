import { create } from "zustand";

import { api } from "@/api/client";
import { PlantStore } from "@/storage/sqlite";
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
      const [remotePlants, schedule] = await Promise.all([
        api.plants.list(),
        api.schedules.merged(),
      ]);
      PlantStore.save(remotePlants);
      set({ plants: remotePlants, schedule, loading: false });
    } catch (error) {
      console.warn("Falling back to offline cache", error);
      const cached = PlantStore.list();
      set({ plants: cached, loading: false });
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

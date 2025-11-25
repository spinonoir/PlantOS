export type LightLevel = "low" | "medium" | "high";

export type Plant = {
  id: string;
  name: string;
  species?: string;
  light_level: LightLevel;
  watering_interval_days: number;
  feeding_interval_days: number;
  reminders_enabled: boolean;
  notes?: string;
  tags: string[];
  created_at?: string;
  updated_at?: string;
};

export type CareTask = {
  id: string;
  plant_id: string;
  signal: string;
  next_due_at: string;
  priority: "low" | "medium" | "high";
};

export type TimelineEvent = {
  id: string;
  plant_id: string;
  event_type: string;
  note: string;
  photo_url?: string;
  created_at: string;
};

export type ScheduleDay = {
  date: string;
  tasks: CareTask[];
};

export type ExperimentVariant = {
  id: string;
  name: string;
  description: string;
  metric: number;
};

export type Experiment = {
  id: string;
  hypothesis: string;
  metric_name: string;
  variants: ExperimentVariant[];
  created_at: string;
  status: string;
};

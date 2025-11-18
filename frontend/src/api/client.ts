const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:8000";

type RequestOptions = Omit<RequestInit, "body"> & { body?: unknown };

async function request<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers ?? {}),
  };
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json() as Promise<T>;
}

export const api = {
  plants: {
    list: () => request("/plants"),
    create: (payload: Record<string, unknown>) =>
      request("/plants", { method: "POST", body: payload }),
    tasks: (plantId: string) => request(`/plants/${plantId}/tasks`),
    timeline: (plantId: string) => request(`/plants/${plantId}/timeline`),
    addTimeline: (plantId: string, payload: Record<string, unknown>) =>
      request(`/plants/${plantId}/timeline`, { method: "POST", body: payload }),
  },
  schedules: {
    merged: (horizonDays = 7) =>
      request(`/schedules/merged?horizon_days=${horizonDays}`),
    due: () => request("/plants/tasks/due"),
  },
  ai: {
    identify: (payload: Record<string, unknown>) =>
      request("/ai/identify", { method: "POST", body: payload }),
    health: (payload: Record<string, unknown>) =>
      request("/ai/health", { method: "POST", body: payload }),
  },
  marketplace: {
    listings: () => request("/marketplace/listings"),
  },
  experiments: {
    list: () => request("/experiments"),
  },
};

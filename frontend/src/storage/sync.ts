import { PlantStore, TaskStore, EventStore } from "./sqlite";

const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000";

export const SyncAdapter = {
    async pull() {
        try {
            // 1. Fetch Plants
            const plantsResp = await fetch(`${API_URL}/plants`);
            if (plantsResp.ok) {
                const plants = await plantsResp.json();
                PlantStore.save(plants);
            }

            // 2. Fetch Tasks (for all plants, or we could do per plant if API supported it)
            // For now, let's assume we fetch all tasks via the due endpoint or similar, 
            // but ideally we need a "sync" endpoint.
            // Since we don't have a bulk task fetch, we might skip this or iterate.
            // Actually, let's iterate over plants to get tasks.
            const plants = PlantStore.list();
            for (const plant of plants) {
                const tasksResp = await fetch(`${API_URL}/plants/${plant.id}/tasks`);
                if (tasksResp.ok) {
                    const tasks = await tasksResp.json();
                    TaskStore.save(tasks);
                }
            }

            console.log("Sync pull completed");
        } catch (error) {
            console.error("Sync pull failed:", error);
        }
    },

    async push() {
        // Implement push logic here (send local changes to backend)
        // For MVP, we might just rely on immediate API calls + optimistic updates,
        // so "push" might just be re-trying failed requests.
        // Leaving this empty for now as we focus on "Pull" for offline cache.
        console.log("Sync push (not implemented)");
    }
};

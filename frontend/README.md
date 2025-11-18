# PlantOS Frontend (Expo)

React Native application built with Expo SDK 51. Delivers plant management, AI diagnostics, experiment insights, propagation inventory, and marketplace browsing.

## Getting Started

```bash
cd frontend
npm install
npm run start           # expo start --offline
npm run lint
```

Environment overrides:

- `EXPO_PUBLIC_API_URL` – point to the FastAPI base URL (default `http://localhost:8000`)

## Architecture

- **Navigation:** React Navigation (bottom tabs + modal stack)
- **State:** Zustand store (`src/store/plantStore.ts`) with SQLite persistence via `expo-sqlite/next`
- **Notifications:** `expo-notifications` bootstrap + helper hook
- **API:** `src/api/client.ts` wraps backend routes for plants, schedules, AI, experiments, marketplace
- **UI:** Shared components in `src/components/`, theming in `src/theme/` with dark-mode support

Screens:

- `Home` – plant list + pull-to-refresh + quick add shortcut  
- `PlantDetail` – tasks, timeline logging, schedule view  
- `Diagnostics` – LangGraph health checks  
- `Experiments` – displays backend experiment runs  
- `Marketplace` – propagation-backed listings snapshot  

## Testing & Linting

```bash
npm run lint
```

CI mirrors the same command (`.github/workflows/lint.yml`).

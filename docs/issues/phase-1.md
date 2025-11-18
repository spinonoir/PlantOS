# Phase 1 – Care Tracker MVP Issues

## P1.1 Firestore Schemas & Serializers
- **Branch:** `feature/P1.1-firestore-models`
- **Areas:** `backend/plantos_backend/models/`, `schemas/`, `storage/`
- **Checklist:**
  - [ ] Define Firestore collection layout for plants, tasks, reminders, timeline events.
  - [ ] Update Pydantic models with Firestore metadata, add conversion helpers.
  - [ ] Document schema in `docs/spec/v1.0/PLANT-OS_SPEC.md`.
  - [ ] Tests cover serialization/deserialization.
- **Labels:** `phase:care-tracker`, `type:backend`

## P1.2 Care Schedule API + Reminder Worker
- **Branch:** `feature/P1.2-care-schedule-api`
- **Areas:** `routers/plants.py`, `services/scheduler.py`, `services/reminders.py`
- **Checklist:**
  - [ ] Expose CRUD for plants + tasks + due-task feed.
  - [ ] Add reminder job (stub) with enqueue logic for OS notifications.
  - [ ] Update API docs + sample requests.
  - [ ] Tests: scheduler forecast, reminder window, FastAPI endpoints.
- **Labels:** `phase:care-tracker`, `type:backend`

## P1.3 Offline Cache & Sync Adapter
- **Branch:** `feature/P1.3-offline-cache`
- **Areas:** `frontend/src/store/plantStore.ts`, `src/storage/sqlite.ts`
- **Checklist:**
  - [ ] Implement conflict resolution + timestamp merges.
  - [ ] Background sync stub bridging API endpoints.
  - [ ] Document offline strategy in README + spec.
  - [ ] Add Jest tests when harness is available (placeholder: unit tests for serialization functions).
- **Labels:** `phase:care-tracker`, `type:frontend`

## P1.4 Timeline UI + Notification Bridge
- **Branch:** `feature/P1.4-timeline-ui`
- **Areas:** `frontend/src/screens/PlantDetailScreen.tsx`, `src/hooks/useNotifications.ts`
- **Checklist:**
  - [ ] Timeline list renders historical events + photos (once available).
  - [ ] Add ability to log events + trigger local notification for due tasks.
  - [ ] Provide screenshots in PR.
  - [ ] Update onboarding docs with notification permissions notes.
- **Labels:** `phase:care-tracker`, `type:frontend`, `type:ui`

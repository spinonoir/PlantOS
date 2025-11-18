# Phase 2 – AI Diagnostics & Experiments Issues

## P2.1 LangGraph Orchestrators & Provider Routing
- **Branch:** `feature/P2.1-langgraph`
- **Areas:** `backend/plantos_backend/ai/graphs.py`, `services/ai.py`, config
- **Checklist:**
  - [ ] Implement provider router supporting OpenAI, Anthropic, Google (mock creds for dev).
  - [ ] Add env vars + `.env.example` entries.
  - [ ] Tests cover graph invocation + fallback path.
  - [ ] Docs describe how to plug in API keys securely.
- **Labels:** `phase:ai`, `type:backend`

## P2.2 Photo Upload + Diagnosis UI
- **Branch:** `feature/P2.2-diagnostics-ui`
- **Areas:** `frontend/src/screens/DiagnosticsScreen.tsx`, media utilities
- **Checklist:**
  - [ ] Add camera/MediaLibrary picker + upload to backend (or mock).
  - [ ] Show progress indicator + AI response state machine.
  - [ ] Update README with screenshot + instructions.
- **Labels:** `phase:ai`, `type:frontend`, `type:ui`

## P2.3 Experiment API + Metrics Logging
- **Branch:** `feature/P2.3-experiment-api`
- **Areas:** `routers/experiments.py`, `services/experiments.py`, `schemas/experiments.py`
- **Checklist:**
  - [ ] CRUD for experiments + variants + metric logs.
  - [ ] Firestore integration plan and migration doc.
  - [ ] Tests for metrics logging + winner selection.
- **Labels:** `phase:ai`, `type:backend`

## P2.4 Experiment Insights Screen
- **Branch:** `feature/P2.4-experiment-insights`
- **Areas:** `frontend/src/screens/ExperimentsScreen.tsx`, chart components
- **Checklist:**
  - [ ] Visualize metrics via Victory/Reanimated charts.
  - [ ] Filter by plant, variant, time range.
  - [ ] Document analytics examples in spec + README.
- **Labels:** `phase:ai`, `type:frontend`, `type:ui`

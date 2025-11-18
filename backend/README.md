# PlantOS Backend

FastAPI service built with `uv` that orchestrates plant care, LangGraph workflows, experiments, propagation, and marketplace flows.

## Tech Stack

- **Runtime:** Python 3.13 + FastAPI + Pydantic  
- **AI:** LangGraph + LangChain for `PlantOnboardGraph`, `HealthCheckGraph`, and experiment scoring  
- **Data layer:** Firestore adapter (planned) and in-memory store for local prototypes  
- **Payments:** Stripe Connect scaffolding (webhook + onboarding stubs)  
- **Async / workers:** Cloud Tasks / Celery (future)  
- **Linting & tests:** Ruff + Pytest (`uv run ruff check`, `uv run pytest`)  

## Development

```bash
cd backend/plantos_backend
uv sync --all-extras --dev
uv run fastapi dev plantos_backend.app:app --reload

# Lint & tests
uv run ruff check src
uv run pytest
```

Key packages live in `src/plantos_backend`:

- `models/` – typed entities for plants, experiments, propagation, marketplace  
- `repositories/` – in-memory store today, designed for Firestore adapters  
- `services/` – schedule optimizer, reminders, AI orchestration, experiments, marketplace  
- `ai/graphs.py` – LangGraph definitions for onboarding, health checks, experiments  
- `routers/` – REST surface: `/plants`, `/schedules`, `/ai`, `/experiments`, `/propagation`, `/marketplace`

Environment variables (see `.env.example`) are loaded via `pydantic-settings` with the `PLANTOS_` prefix.
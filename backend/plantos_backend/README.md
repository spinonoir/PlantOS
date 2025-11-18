# plantos-backend

FastAPI + LangGraph prototype for PlantOS. Managed entirely with [uv](https://github.com/astral-sh/uv).

## Commands

```bash
uv sync --all-extras --dev      # install deps + ruff + pytest
uv run fastapi dev plantos_backend.app:app --reload
uv run ruff check src
uv run pytest
```

## Layout

- `app.py` – FastAPI factory with CORS + router auto-registration
- `routers/` – API surface (`/plants`, `/schedules`, `/ai`, `/experiments`, `/propagation`, `/marketplace`)
- `models/` – Pydantic domain objects (plants, tasks, experiments, marketplace, propagation)
- `services/` – schedule optimizer, reminders, LangGraph orchestration, marketplace logic
- `ai/graphs.py` – `PlantOnboardGraph`, `HealthCheckGraph`, `ExperimentGraph`
- `storage/memory.py` – in-memory backing store for local prototypes (swap with Firestore later)
- `tests/` – Pytest coverage for scheduler + core APIs

Set environment overrides via `.env` (see `.env.example`). All settings are prefixed with `PLANTOS_`.

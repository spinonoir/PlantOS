# PlantOS  
_Intelligent Plant Care, Experimentation & Marketplace_

PlantOS is a cross-platform system for tracking plants, optimizing their care with AI, running experiments on different care strategies, and buying/selling/trading plants through a built-in marketplace.

It’s designed for hobbyists, collectors, and small growers who want structured plant care, powerful analytics, and an ecosystem for propagation and resale.

---

## Features

- **Smart plant onboarding**
  - Add a plant with photos and metadata.
  - Use external plant ID APIs + LLMs to guess species and care requirements.
  - Auto-generate light, watering, feeding, and pruning guidelines.

- **Care schedules & reminders**
  - Per-plant care profiles with history of events.
  - Schedule optimizer that groups tasks across plants (e.g., all 2-week plants on the same day).
  - Offline-capable reminders via local notifications.

- **AI health checks**
  - Upload photos to detect stress, pests, or disease using vision models.
  - LLM synthesizes diagnostics + recommended actions.
  - (Future) Feedback loop tying actions to outcomes.

- **Experiments / A/B testing**
  - Plant-level experiments (e.g., watering frequency, fertilizer, light levels).
  - System-level experiments (e.g., which LLM provider, which prompt template).
  - Metrics tracking for growth, incidents, care adherence, AI performance.

- **Propagation & nursery tools**
  - Mark “mother plants” and create propagation batches.
  - Track children through stages (cutting → rooted → acclimatized → sale-ready).
  - Convert plants to inventory items with cost and price.

- **Marketplace**
  - Any user can create a seller profile and list plants or cuttings for sale/trade.
  - Listings link back to real plant records and optional provenance history.
  - Orders, trades, and reviews with platform-level commission support.
  - Planned payment integration via Stripe Connect.

- **Data & insights**
  - Event timelines and photo history per plant.
  - Aggregated analytics for experiments and marketplace.
  - Architecture designed for future ML training on opt-in, anonymized data.

---

## High-Level Architecture

- **Frontend**
  - React Native + Expo (iOS / Android, web optional).
  - Offline-first data layer (SQLite/WatermelonDB) synchronized with Firestore.
  - Local notifications for care reminders.

- **Backend**
  - FastAPI (Python) REST API.
  - Firebase Firestore + Cloud Storage for structured and media data.
  - LangGraph / LangChain for AI orchestration:
    - Plant onboarding
    - Schedule optimization
    - Health diagnostics
    - Shopping/fit advisor
    - Experiment management
  - Stripe Connect (planned) for marketplace payments.
  - BigQuery / analytics tool for metrics and A/B testing.

- **AI / External APIs**
  - Plant ID & ailment detection providers (e.g., Plant.id, Plant.health).
  - LLM providers: OpenAI, Anthropic, Google, etc. behind a router node.
  - MCP Servers (Model Context Protocol) for modular tool access (future).

---

## Repository Structure

```text
PlantOS/
├─ backend/
│  └─ plantos_backend/        # FastAPI + LangGraph service (uv-managed)
├─ docs/
│  ├─ spec/v1.0/              # Living architecture + roadmap
│  └─ product/                # Product brief / positioning
├─ frontend/                  # Expo app with offline cache + AI flows
├─ third_party/NOTES.md       # OSS attributions & intake log
├─ .github/workflows/         # Lint + CI automation
├─ LICENSE                    # Dual license (MIT frontend / proprietary backend)
└─ README.md
```

---

## Getting Started

### Requirements

- [uv](https://github.com/astral-sh/uv) for Python environments (no pyenv required)  
- Node.js 20.x + npm  
- Expo CLI (`npx expo start`)  

### Backend (FastAPI + LangGraph)

```bash
cd /Users/jarret/Documents/projects/PlantOS/backend/plantos_backend
uv sync --all-extras --dev
uv run fastapi dev plantos_backend.app:app --reload

# Run tests + lint
uv run pytest
uv run ruff check src
```

Key endpoints:

- `GET /health` – readiness probe  
- `POST /plants` – plant CRUD + schedule generation  
- `GET /schedules/merged` – merged care tasks per day  
- `POST /ai/identify` / `/ai/health` – LangGraph-backed prototypes  
- `POST /marketplace/listings` & `/orders` – marketplace stubs for Stripe integration  

### Frontend (Expo + offline cache)

```bash
cd /Users/jarret/Documents/projects/PlantOS/frontend
npm install
npm run start          # expo start --offline
npm run lint
```

Highlights:

- React Navigation tabs for Plants, Diagnostics, Experiments, Marketplace  
- Zustand store with SQLite persistence (`expo-sqlite/next`)  
- Local notifications bootstrapped via `expo-notifications`  
- API client pointed at `http://localhost:8000` by default (override `EXPO_PUBLIC_API_URL`)  

### Continuous Integration

`.github/workflows/lint.yml` runs:

- `uv run ruff check` + `uv run pytest` inside `backend/plantos_backend`  
- `npm install && npm run lint` inside `frontend/`  

### Git & Issue Workflow

1. Keep `master` clean and pushed (`git status`, `git push origin master`) before opening new work.
2. Open a GitHub issue using the templates in `docs/issues/`. Each issue maps to a branch named `feature/<issue-id>-<slug>` (e.g., `feature/P1.2-care-schedule-api`).
3. Implement the change, run tests (`uv run ruff check`, `uv run pytest`, `npm run lint`), and update docs (`README.md`, `PlantOS_BOOTSTRAP.md`, `docs/spec/v1.0/PLANT-OS_SPEC.md`).
4. Push the branch, open a PR referencing the issue, list verification steps/screenshots, and squash-merge back to `master`.
5. Update `docs/issues/` and CHANGELOG entries as issues close; tag releases at the end of every phase.

### OSS Intake & Licensing

- Track every copied snippet + license in `third_party/NOTES.md`.  
- Frontend code is MIT licensed; backend + infrastructure is covered by the PlantOS proprietary license (see `LICENSE`).  Third-party components keep their upstream licenses.

---

## Status

- ✅ Phase 0: Repo bootstrap, FastAPI health route, Expo scaffolding, CI linting  
- 🚧 Phase 1: Plant CRUD, schedule optimization, offline reminders (prototype delivered)  
- 🔬 Phase 2: LangGraph identification / diagnostics + experiment wiring (prototype delivered)  
- 🛒 Phase 3: Propagation → marketplace listings + Stripe stubs (prototype delivered)  

See `docs/spec/v1.0/PLANT-OS_SPEC.md` and `PlantOS_BOOTSTRAP.md` for the full roadmap.

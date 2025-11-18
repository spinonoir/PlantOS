# PlantOS Development Bootstrap Guide

This document provides a high-level overview of how to prepare the initial phase of the PlantOS project for active development. It focuses on identifying relevant open‑source repositories, how those repositories should be incorporated into the project structure, how to handle forks and licenses, and how to establish a coherent development foundation using your preferred toolchain (including Python environment management via `uv`).

This document is intentionally high-level because it will be consumed by a planning agent that will determine phases, tasks, and work breakdown automatically.

---

## 1. Goals of the Bootstrap Phase

The objective of the bootstrap phase is to establish:

- The initial directory structure of the PlantOS repository.
- The selection and placement of external open‑source scaffolding.
- The strategy for integrating OSS code into PlantOS while managing forks, updates, and licenses.
- The high-level approach to setting up backend and frontend foundations.
- The method for incorporating libraries and third‑party services without over‑specifying implementation details.
- A clear separation between PlantOS‑owned code, third‑party reference code, and external dependencies.

This phase does **not** involve detailed implementation. Instead, it defines the structure and conventions the project will rely on once development begins.

---

## 2. Project Hierarchy Overview

PlantOS will use a unified monorepo with a structure similar to:

```
PlantOS/
├─ docs/
│  ├─ spec/
│  └─ product/
├─ backend/
│  └─ (FastAPI + LangGraph code)
├─ frontend/
│  └─ (React Native / Expo code)
├─ third_party/
│  └─ (notes and retained OSS license files)
├─ .gitignore
├─ README.md
└─ LICENSE
```

No external repository will be nested directly under PlantOS except for one-time imports or small internal copies. Third‑party repos will be referenced, not fully embedded.

---

## 3. Open‑Source Repositories to Use as Scaffolding

PlantOS bootstrapping relies on several OSS repositories. Each serves a different purpose.

### 3.1 Smart Plant Care Assistant (Frontend Scaffold)

URL: https://github.com/BaratKarla/Smart-Plant-Care-Assistant

Purpose:
Provides a minimal React Native application with plant CRUD, navigation structure, and photo capture integration. This will serve as a starting point for the `frontend/` folder.

Integration Approach:
Fork the repository in your GitHub account, clone it separately, and copy selected components into `frontend/`. After the initial copy, PlantOS will diverge from upstream, and no ongoing sync is expected.

---

### 3.2 HortusFox (Data Model Inspiration)

URL: https://github.com/llcooluk/HortusFox

Purpose:
Inspires the design of PlantOS plant, event, and propagation data structures.

Integration Approach:
Clone locally in a separate workspace. Do not fork or embed. Reference its concepts while designing backend collection schemas.

---

### 3.3 Stripe Marketplace Examples (Commerce Flow Reference)

URLs:
- https://github.com/stripe-samples/connect-onboarding-for-standard
- https://github.com/stripe/stripe-react-native/tree/master/example

Purpose:
Provide patterns for seller onboarding, checkout flows, and platform fee handling.

Integration Approach:
Reference-only. Copy patterns as needed into backend and frontend implementations later.

---

### 3.4 LangGraph / LangChain Examples (AI Pipeline Structure)

URL: https://github.com/langchain-ai/langgraph

Purpose:
Supply reference workflows for orchestrating multi-step AI pipelines, including routing between providers.

Integration Approach:
Treat as a reference and install via `uv add langgraph langchain`. No forking required.

---

### 3.5 Expo Firebase Starter (Mobile Firebase Integration)

URL: https://github.com/expo-community/expo-firebase-starter

Purpose:
Provides patterns for Expo-based Firebase initialization, auth, and Firestore interactions.

Integration Approach:
Reference-only. Selectively copy setup utilities into PlantOS frontend.

---

## 4. Forking, Syncing, and Integration Strategy

PlantOS uses a hybrid approach to OSS integration:

### 4.1 Fork-and-Copy (One-Time Imports)

Used for:
- Smart Plant Care Assistant

Process:
1. Fork the repo in your GitHub account.
2. Clone the fork separately.
3. Copy selected files into `frontend/`.
4. After copying, PlantOS does not maintain a relationship with the upstream project.
5. Upstream updates may be manually inspected and selectively incorporated.

### 4.2 Reference-Only Repos

Used for:
- HortusFox
- Stripe sample repos
- Expo Firebase starter
- LangGraph examples (though installed as a library)

These remain separate and are not forked or embedded. They inform architecture and implementation but do not directly contribute code.

### 4.3 Library Dependencies

Handled primarily via:
- uv for Python
- npm/yarn/pnpm for JavaScript

Libraries such as LangGraph, LangChain, Firebase SDKs, and Stripe SDKs will be installed normally and version-pinned via dependency files.

---

## 5. License Management

PlantOS will eventually have multiple sources of intellectual property. To manage this correctly:

### 5.1 Primary License

PlantOS will maintain:
- A top-level LICENSE file for its own code.
- Additional internal licensing policies (backend proprietary, frontend MIT).

### 5.2 Third‑Party Licenses

Any OSS code copied into PlantOS must:
- Retain its original copyright.
- Retain its original license header.
- Be documented in `third_party/NOTES.md`.

### 5.3 Library Licenses

Dependencies installed via package managers already include license metadata. No further action is required unless distributing binaries.

---

## 6. Backend Foundation Setup (High-Level)

### 6.1 Using uv for Python environment management

The backend will use:

```
uv init
uv add fastapi uvicorn langgraph langchain openai anthropic google-generativeai
uv add google-cloud-firestore google-cloud-storage stripe python-dotenv
```

PlantOS backend will be structured into high-level domains such as:

- API routes
- AI orchestration (LangGraph)
- Marketplace/payment services
- Data models referencing Firestore collections

The bootstrap phase does not specify implementation.

---

## 7. Frontend Foundation Setup (High-Level)

The frontend will use:

- React Native (Expo)
- Firebase SDK
- Stripe React Native
- Navigation and state management libraries

The Smart Plant Care Assistant provides initial scaffolding for:
- Navigation
- Plant listing UI
- Camera and media handling

The Expo Firebase starter informs:
- Firebase initialization patterns
- Auth integration
- Firestore read/write approach

Specific implementation will be deferred to future phases.

---

## 8. Third‑Party Services

PlantOS will support integration with:

- Plant identification APIs
- LLMs via LangGraph routing
- Stripe for marketplace payments
- Firebase for auth, storage, and syncing

This document does not specify configuration details, because they will be determined in later planning phases.

---

## 9. Summary

The bootstrap phase of PlantOS focuses on establishing:

- A clean folder hierarchy
- A strategy for consuming open‑source scaffolding
- Clear boundaries between copied code, reference code, and installed libraries
- A sustainable licensing and attribution system
- High-level backend and frontend foundations
- A plan for using uv for environment and dependency management
- A reproducible pattern for integrating AI, Firebase, and Stripe technologies

This sets the foundation for later phases where a planning agent will define concrete tasks, milestones, and implementation steps.

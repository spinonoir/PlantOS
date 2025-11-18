# GitHub Issue & Branch Workflow

1. **Always push `master` before opening a new issue.** Use `git status` to ensure a clean tree.
2. **Create the issue on GitHub** using the text snippets in the phase markdown files (P0–P3). Copy the title, description, acceptance checklist, and labels.
3. **Create a feature branch** named `feature/<issue-id>-<slug>`. Example: `feature/P1.2-care-schedule-api`.
4. **Implement + test.**
   - Backend: `uv run ruff check` + `uv run pytest`
   - Frontend: `npm run lint`
5. **Update docs** (`README.md`, `PlantOS_BOOTSTRAP.md`, `docs/spec/v1.0/PLANT-OS_SPEC.md`, `docs/issues/*.md`) to reflect changes.
6. **Commit with conventional message** (e.g., `feat: add care schedule API`).
7. **Push branch and open PR** referencing the issue (`Fixes #<issue-number>`), include verification steps, screenshots/logs, and doc links.
8. **Squash merge** via GitHub, delete branch, and move the issue to `Done`.
9. **Update CHANGELOG** (to be added) and tag releases at the end of each phase (`v0.1.0`, `v0.2.0`, ...).

Use the phase-specific files below to create issues:

- `phase-0.md` – Bootstrap & GitOps
- `phase-1.md` – Care Tracker MVP
- `phase-2.md` – AI Diagnostics & Experiments
- `phase-3.md` – Marketplace & Monetization

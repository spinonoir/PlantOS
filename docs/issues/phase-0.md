# Phase 0 – Bootstrap & GitOps Issues

## P0.1 Push Baseline & Document Workflow
- **Branch:** `feature/P0.1-git-workflow`
- **Summary:** Push the current repository state to GitHub, document the workflow in `README.md` and `PlantOS_BOOTSTRAP.md`, and ensure contributors know how to branch, test, and merge.
- **Checklist:**
  - [ ] Confirm `master` clean & pushed (`git push origin master`).
  - [ ] Add "Git & Issue Workflow" section to `README.md`.
  - [ ] Add Git process primer to `PlantOS_BOOTSTRAP.md`.
  - [ ] Link to `docs/issues/` directory.
  - [ ] PR references this issue and lists verification commands.
- **Labels:** `phase:bootstrap`, `type:docs`, `priority:high`

## P0.2 Verify uv/Expo Bootstrap Instructions
- **Branch:** `feature/P0.2-bootstrap-instructions`
- **Checklist:**
  - [ ] Run backend setup commands and note prerequisites.
  - [ ] Run frontend setup (`npm install`, `npm run start`).
  - [ ] Update `README.md` + `PlantOS_BOOTSTRAP.md` troubleshooting.
  - [ ] Add checklist of verification commands to docs.
- **Labels:** `phase:bootstrap`, `type:docs`, `type:devops`

## P0.3 Licensing & OSS Intake Guardrails
- **Branch:** `feature/P0.3-licensing`
- **Checklist:**
  - [ ] Confirm `LICENSE` documents dual-license stance.
  - [ ] Expand `third_party/NOTES.md` with intake rules + attribution steps.
  - [ ] Ensure copied code retains upstream notices.
- **Labels:** `phase:bootstrap`, `type:legal`

## P0.4 CI Lint & Test Workflow
- **Branch:** `feature/P0.4-ci-lint`
- **Checklist:**
  - [ ] Verify `.github/workflows/lint.yml` passes locally via `act` or dry-run.
  - [ ] Document required secrets (if any) and caching strategy.
  - [ ] Ensure workflow runs `uv run ruff check`, `uv run pytest`, `npm run lint`.
  - [ ] Update `README.md` Continuous Integration section with badges once available.
- **Labels:** `phase:bootstrap`, `type:ci`

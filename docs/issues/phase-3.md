# Phase 3 – Marketplace & Monetization Issues

## P3.1 Propagation Inventory & Listing Eligibility
- **Branch:** `feature/P3.1-propagation`
- **Areas:** `services/propagation.py`, `/propagation` router, Firestore schemas
- **Checklist:**
  - [ ] Implement propagation batch lifecycle + readiness checks.
  - [ ] Auto-suggest listing creation when batch `sale_ready`.
  - [ ] Update docs/spec with propagation-to-marketplace data flow.
- **Labels:** `phase:marketplace`, `type:backend`

## P3.2 Stripe Connect Onboarding & Webhooks
- **Branch:** `feature/P3.2-stripe-connect`
- **Areas:** `backend/payments/` (new), webhook handlers, env docs
- **Checklist:**
  - [ ] Implement Stripe Connect onboarding flow (test mode).
  - [ ] Handle payout + order webhooks with signature verification.
  - [ ] Provide local webhook replay instructions (`stripe listen`).
- **Labels:** `phase:marketplace`, `type:backend`, `type:payments`

## P3.3 Marketplace UI Flows
- **Branch:** `feature/P3.3-marketplace-ui`
- **Areas:** `frontend/src/screens/MarketplaceScreen.tsx`, new listing flow components
- **Checklist:**
  - [ ] Allow growers to publish listings from sale-ready batches.
  - [ ] Implement checkout mock + order confirmation view.
  - [ ] Add screenshots + README instructions.
- **Labels:** `phase:marketplace`, `type:frontend`, `type:ui`

## P3.4 Provenance Visualization
- **Branch:** `feature/P3.4-provenance`
- **Areas:** `frontend/src/components/ProvenanceTimeline.tsx` (new), backend provenance endpoints
- **Checklist:**
  - [ ] Expose provenance API joining propagation + marketplace data.
  - [ ] Visualize lineage chain + metadata per listing.
  - [ ] Document provenance feature in spec + marketing copy.
- **Labels:** `phase:marketplace`, `type:fullstack`

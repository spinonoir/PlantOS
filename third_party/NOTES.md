# Third-Party Reference & Intake Log

| Source | License (verify upstream) | Purpose | Integration Strategy |
|--------|---------------------------|---------|----------------------|
| [Smart Plant Care Assistant](https://github.com/BaratKarla/Smart-Plant-Care-Assistant) | MIT (confirm before copying) | React Native navigation + plant CRUD starter | Fork once, copy patterns into `frontend/` and document changes here. |
| [HortusFox](https://github.com/llcooluk/HortusFox) | GPL-3.0 (confirm) | Data model inspiration for plants/propagation | Reference only; no code copied. |
| [Stripe Connect Onboarding Sample](https://github.com/stripe-samples/connect-onboarding-for-standard) | MIT | Marketplace onboarding flow | Reference-only; inform backend Stripe integration. |
| [Stripe React Native Example](https://github.com/stripe/stripe-react-native/tree/master/example) | MIT | Client-side checkout flows | Reference-only; selectively adapt UI components. |
| [Expo Firebase Starter](https://github.com/expo-community/expo-firebase-starter) | MIT | Firebase auth + Firestore scaffolding | Reference-only utilities for auth/sync layers. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Apache-2.0 | AI orchestration graphs | Installed via `uv`; adhere to upstream license notice in release notes. |

When copying source code, include license headers in the target file and append a note to this table with commit hash + path.

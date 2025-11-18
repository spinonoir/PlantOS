"""LangGraph workflows for PlantOS prototypes."""
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class PlantOnboardState(TypedDict, total=False):
    photo_url: str | None
    notes: str | None
    species_guess: str
    confidence: float
    care_profile: dict


def identify_species(state: PlantOnboardState) -> PlantOnboardState:
    notes = (state.get("notes") or "").lower()
    if "fern" in notes:
        species = "Boston Fern"
        confidence = 0.81
    elif "succulent" in notes:
        species = "Haworthia Fasciata"
        confidence = 0.74
    else:
        species = "Monstera Deliciosa"
        confidence = 0.7
    state.update({"species_guess": species, "confidence": confidence})
    return state


def build_care_profile(state: PlantOnboardState) -> PlantOnboardState:
    species = state.get("species_guess", "Unknown")
    care_profile = {
        "species": species,
        "light": "bright indirect" if "Monstera" in species else "medium",
        "watering_days": 7 if "succulent" not in species.lower() else 14,
        "feeding_days": 30,
    }
    state["care_profile"] = care_profile
    return state


plant_onboard_graph = StateGraph(PlantOnboardState)
plant_onboard_graph.add_node("identify", identify_species)
plant_onboard_graph.add_node("profile", build_care_profile)
plant_onboard_graph.add_edge(START, "identify")
plant_onboard_graph.add_edge("identify", "profile")
plant_onboard_graph.add_edge("profile", END)
PLANT_ONBOARD_GRAPH = plant_onboard_graph.compile()


class HealthCheckState(TypedDict, total=False):
    description: str
    diagnosis: str
    severity: str
    recommendations: list[str]


def run_diagnostics(state: HealthCheckState) -> HealthCheckState:
    description = (state.get("description") or "").lower()
    if "yellow" in description:
        diagnosis = "Possible overwatering"
        recommendations = ["Allow soil to dry", "Check drainage"]
    elif "brown" in description:
        diagnosis = "Low humidity"
        recommendations = ["Mist leaves", "Add pebble tray"]
    else:
        diagnosis = "Stable"
        recommendations = ["Monitor"]
    state.update({"diagnosis": diagnosis, "recommendations": recommendations, "severity": "medium"})
    return state


health_graph = StateGraph(HealthCheckState)
health_graph.add_node("diagnose", run_diagnostics)
health_graph.add_edge(START, "diagnose")
health_graph.add_edge("diagnose", END)
HEALTH_CHECK_GRAPH = health_graph.compile()


class ExperimentState(TypedDict, total=False):
    hypothesis: str
    metric: str
    variants: list[dict]


def evaluate_variants(state: ExperimentState) -> ExperimentState:
    variants = state.get("variants", [])
    for idx, variant in enumerate(variants):
        variant.setdefault("metric", 0.5 + (idx * 0.1))
    return state


experiment_graph = StateGraph(ExperimentState)
experiment_graph.add_node("score", evaluate_variants)
experiment_graph.add_edge(START, "score")
experiment_graph.add_edge("score", END)
EXPERIMENT_GRAPH = experiment_graph.compile()

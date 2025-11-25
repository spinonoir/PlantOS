"""LangGraph workflows for PlantOS prototypes."""
from __future__ import annotations

from typing import TypedDict

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from plantos_backend.ai.providers import get_provider


class PlantOnboardState(TypedDict, total=False):
    photo_url: str | None
    notes: str | None
    species_guess: str
    confidence: float
    care_profile: dict


def identify_species(state: PlantOnboardState) -> PlantOnboardState:
    """Identify plant species from notes (and eventually photo)."""
    notes = state.get("notes") or ""
    
    # In a real scenario, we would pass the photo_url to a vision model.
    # For now, we use the text notes with the LLM.
    provider = get_provider()
    model = provider.get_chat_model()
    
    prompt = f"""
    Identify the plant species based on the following user notes:
    "{notes}"
    
    Return ONLY the species name. If you are unsure, return "Unknown".
    """
    
    response = model.invoke([HumanMessage(content=prompt)])
    species = response.content.strip()
    
    # Mock confidence for now as most chat models don't return it easily without logprobs
    confidence = 0.9 if species != "Unknown" else 0.0
    
    state.update({"species_guess": species, "confidence": confidence})
    return state


def build_care_profile(state: PlantOnboardState) -> PlantOnboardState:
    """Generate a care profile for the identified species."""
    species = state.get("species_guess", "Unknown")
    
    if species == "Unknown":
        return state

    provider = get_provider()
    model = provider.get_chat_model()
    
    # We want structured output, but for simplicity we'll parse JSON or just ask for specific fields.
    # Let's ask for a JSON string.
    prompt = f"""
    Generate a care profile for "{species}" in JSON format with the following keys:
    - light: (e.g., "bright indirect", "low")
    - watering_days: (integer, frequency in days)
    - feeding_days: (integer, frequency in days)
    
    Return ONLY the JSON.
    """
    
    response = model.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()
    
    # Basic cleanup to handle markdown code blocks if present
    if content.startswith("```json"):
        content = content[7:-3]
    elif content.startswith("```"):
        content = content[3:-3]
        
    import json
    try:
        care_profile = json.loads(content)
        care_profile["species"] = species
        state["care_profile"] = care_profile
    except json.JSONDecodeError:
        # Fallback or error handling
        pass
        
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
    description = state.get("description") or ""
    
    provider = get_provider()
    model = provider.get_chat_model()
    
    prompt = f"""
    Diagnose the plant health issue based on this description:
    "{description}"
    
    Return a JSON object with:
    - diagnosis: Short diagnosis title
    - severity: "low", "medium", or "high"
    - recommendations: list of strings (actions to take)
    
    Return ONLY the JSON.
    """
    
    response = model.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()
    
    if content.startswith("```json"):
        content = content[7:-3]
    elif content.startswith("```"):
        content = content[3:-3]
        
    import json
    try:
        result = json.loads(content)
        state.update({
            "diagnosis": result.get("diagnosis", "Unknown"),
            "severity": result.get("severity", "low"),
            "recommendations": result.get("recommendations", [])
        })
    except json.JSONDecodeError:
        state.update({
            "diagnosis": "Error parsing diagnosis",
            "severity": "unknown",
            "recommendations": []
        })
        
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
    """Mock evaluation of experiment variants using AI to simulate outcomes."""
    hypothesis = state.get("hypothesis")
    variants = state.get("variants", [])
    metric = state.get("metric")
    
    provider = get_provider()
    model = provider.get_chat_model()
    
    for variant in variants:
        variant_desc = variant.get("description", "")
        prompt = f"""
        Simulate an experiment for plant growth.
        Hypothesis: {hypothesis}
        Metric: {metric}
        Variant: {variant_desc}
        
        Predict a likely score for this metric on a scale of 0.0 to 1.0 (float).
        Return ONLY the number.
        """
        
        response = model.invoke([HumanMessage(content=prompt)])
        try:
            score = float(response.content.strip())
        except ValueError:
            score = 0.5
            
        variant["metric"] = score
        
    return state


experiment_graph = StateGraph(ExperimentState)
experiment_graph.add_node("score", evaluate_variants)
experiment_graph.add_edge(START, "score")
experiment_graph.add_edge("score", END)
EXPERIMENT_GRAPH = experiment_graph.compile()

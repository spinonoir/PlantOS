"""Service for managing plant growth experiments."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel

from plantos_backend.ai.graphs import EXPERIMENT_GRAPH


class ExperimentVariant(BaseModel):
    id: str
    name: str
    description: str
    metric: float = 0.0  # Current score/metric value


class Experiment(BaseModel):
    id: str
    hypothesis: str
    metric_name: str
    variants: List[ExperimentVariant]
    created_at: datetime = datetime.now()
    status: str = "running"


# In-memory storage for prototype
_experiments: Dict[str, Experiment] = {}


def create_experiment(hypothesis: str, metric_name: str, variants: List[dict]) -> Experiment:
    experiment_id = str(uuid4())
    experiment_variants = []
    
    for v in variants:
        experiment_variants.append(ExperimentVariant(
            id=str(uuid4()),
            name=v.get("name", "Variant"),
            description=v.get("description", ""),
        ))
        
    experiment = Experiment(
        id=experiment_id,
        hypothesis=hypothesis,
        metric_name=metric_name,
        variants=experiment_variants,
    )
    
    _experiments[experiment_id] = experiment
    return experiment


def list_experiments() -> List[Experiment]:
    return list(_experiments.values())


def get_experiment(experiment_id: str) -> Optional[Experiment]:
    return _experiments.get(experiment_id)


def log_metric(experiment_id: str, variant_id: str, value: float) -> Optional[Experiment]:
    experiment = _experiments.get(experiment_id)
    if not experiment:
        return None
        
    for variant in experiment.variants:
        if variant.id == variant_id:
            variant.metric = value
            break
            
    return experiment


async def simulate_experiment(experiment_id: str) -> Optional[Experiment]:
    experiment = _experiments.get(experiment_id)
    if not experiment:
        return None
        
    # Prepare input for LangGraph
    inputs = {
        "hypothesis": experiment.hypothesis,
        "metric": experiment.metric_name,
        "variants": [v.model_dump() for v in experiment.variants],
    }
    
    # Run simulation
    result = await EXPERIMENT_GRAPH.ainvoke(inputs)
    
    # Update experiment with simulated results
    simulated_variants = result.get("variants", [])
    
    for sim_v in simulated_variants:
        for v in experiment.variants:
            if v.id == sim_v.get("id"):
                v.metric = sim_v.get("metric", 0.0)
                
    return experiment

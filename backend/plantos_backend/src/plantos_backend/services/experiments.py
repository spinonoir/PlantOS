"""Experiment management services."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from plantos_backend.models import Experiment, ExperimentVariant
from plantos_backend.schemas.experiments import ExperimentCreate, ExperimentMetricLog
from plantos_backend.storage.memory import memory_store


def create_experiment(payload: ExperimentCreate) -> Experiment:
    variants = [
        ExperimentVariant(
            label=variant.label,
            description=variant.description,
            parameters=variant.parameters,
        )
        for variant in payload.variants
    ]
    experiment = Experiment(
        name=payload.name,
        hypothesis=payload.hypothesis,
        plant_id=payload.plant_id,
        metric_keys=payload.metric_keys,
        variants=variants,
    )
    memory_store.experiments[experiment.id] = experiment
    return experiment


def list_experiments(plant_id: Optional[str] = None) -> List[Experiment]:
    experiments = list(memory_store.experiments.values())
    if plant_id:
        experiments = [exp for exp in experiments if exp.plant_id == plant_id]
    return experiments


def log_metric(experiment_id: str, payload: ExperimentMetricLog) -> Experiment:
    experiment = memory_store.experiments.get(experiment_id)
    if not experiment:
        raise ValueError("Experiment not found")
    variant = next(
        (variant for variant in experiment.variants if variant.id == payload.variant_id),
        None,
    )
    if not variant:
        raise ValueError("Variant not found")
    metrics = dict(variant.metrics)
    metrics[payload.metric] = payload.value
    updated_variant = variant.model_copy(update={"metrics": metrics})
    variants = [updated_variant if v.id == variant.id else v for v in experiment.variants]
    experiment = experiment.model_copy(update={"variants": variants})
    memory_store.experiments[experiment_id] = experiment
    return experiment


def complete_experiment(experiment_id: str, winning_variant_id: str) -> Experiment:
    experiment = memory_store.experiments.get(experiment_id)
    if not experiment:
        raise ValueError("Experiment not found")
    metadata = dict(experiment.metadata)
    metadata["winner"] = winning_variant_id
    experiment = experiment.model_copy(
        update={"completed_at": datetime.now(timezone.utc), "metadata": metadata}
    )
    memory_store.experiments[experiment_id] = experiment
    return experiment

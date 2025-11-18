"""Schemas for AI endpoints."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class PlantIdentifyRequest(BaseModel):
    photo_url: Optional[str] = None
    notes: Optional[str] = None


class PlantIdentifyResponse(BaseModel):
    species_guess: str
    confidence: float
    care_profile: dict


class HealthCheckRequest(BaseModel):
    description: str


class HealthCheckResponse(BaseModel):
    diagnosis: str
    severity: str
    recommendations: List[str]


class ExperimentReviewRequest(BaseModel):
    hypothesis: str
    variants: List[dict]


class ExperimentReviewResponse(BaseModel):
    variants: List[dict]

"""
Day 23 - Screening Interaction Schema

Defines the structured database representation of
AI-based HR screening interactions.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ScreeningInteractionRecord(BaseModel):
    """
    Represents one question-response interaction
    during an AI screening session.
    """

    interaction_id: str = Field(
        ...,
        description="Unique interaction identifier"
    )

    transcript_id: str = Field(
        ...,
        description="Associated transcript identifier"
    )

    candidate_id: str = Field(
        ...,
        description="Unique candidate identifier"
    )

    job_id: str = Field(
        ...,
        description="Unique job identifier"
    )

    question_id: str = Field(
        ...,
        description="Screening question identifier"
    )

    question_text: str = Field(
        ...,
        description="Question presented to the candidate"
    )

    response_text: str = Field(
        ...,
        description="Candidate response"
    )

    timestamp: float = Field(
        ...,
        ge=0,
        description="Interaction timestamp in seconds"
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Transcript confidence level"
    )

    response_duration_seconds: Optional[float] = Field(
        default=None,
        ge=0,
        description="Duration of candidate response"
    )

    created_at: datetime = Field(
        ...,
        description="Record creation timestamp"
    )

    status: str = Field(
        default="completed",
        description="Interaction status"
    )
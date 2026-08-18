"""
Day 23 - Voice Transcript Data Schema

Defines the standard structure used to store
AI screening voice conversations.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    """
    Represents one spoken segment in a screening conversation.
    """

    speaker: str = Field(
        ...,
        description="Speaker identifier: candidate, interviewer, or system"
    )

    text: str = Field(
        ...,
        description="Normalized transcript text"
    )

    timestamp: float = Field(
        ...,
        ge=0,
        description="Time offset in seconds from the beginning of the conversation"
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Speech-to-text confidence score"
    )


class ScreeningInteraction(BaseModel):
    """
    Represents one question and candidate response.
    """

    question_id: str = Field(
        ...,
        description="Unique screening question identifier"
    )

    question_text: str = Field(
        ...,
        description="Question asked during screening"
    )

    response_text: str = Field(
        ...,
        description="Candidate's normalized response"
    )

    timestamp: float = Field(
        ...,
        ge=0,
        description="Timestamp when the interaction started"
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence in the transcript"
    )


class VoiceTranscript(BaseModel):
    """
    Complete voice screening transcript.
    """

    transcript_id: str = Field(
        ...,
        description="Unique transcript identifier"
    )

    candidate_id: str = Field(
        ...,
        description="Unique candidate identifier"
    )

    job_id: str = Field(
        ...,
        description="Unique job identifier"
    )

    created_at: datetime = Field(
        ...,
        description="Transcript creation timestamp"
    )

    language: str = Field(
        default="en",
        description="Transcript language code"
    )

    duration_seconds: Optional[float] = Field(
        default=None,
        ge=0,
        description="Total conversation duration"
    )

    segments: List[TranscriptSegment] = Field(
        default_factory=list,
        description="Individual transcript segments"
    )

    interactions: List[ScreeningInteraction] = Field(
        default_factory=list,
        description="Question and response pairs"
    )
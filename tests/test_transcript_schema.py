"""
Day 23 - Transcript Schema Tests
"""

import json
from pathlib import Path

from schemas.transcript_schema import VoiceTranscript
from schemas.screening_interaction_schema import ScreeningInteractionRecord


BASE_DIR = Path(__file__).resolve().parents[1]


def test_transcript_schema():
    """
    Validate the sample voice transcript.
    """

    file_path = (
        BASE_DIR
        / "data"
        / "transcripts"
        / "sample_screening_transcript.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    transcript = VoiceTranscript(**data)

    assert transcript.transcript_id == "transcript_001"
    assert transcript.candidate_id == "cand_001"
    assert transcript.job_id == "job_001"
    assert len(transcript.segments) > 0
    assert len(transcript.interactions) > 0


def test_screening_interaction_schema():
    """
    Validate one screening interaction.
    """

    file_path = (
        BASE_DIR
        / "data"
        / "transcripts"
        / "screening_interaction_001.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    interaction = ScreeningInteractionRecord(**data)

    assert interaction.interaction_id == "interaction_001"
    assert interaction.transcript_id == "transcript_001"
    assert interaction.candidate_id == "cand_001"
    assert interaction.job_id == "job_001"
    assert interaction.question_id == "q_001"
    assert 0 <= interaction.confidence <= 1
    assert interaction.timestamp >= 0
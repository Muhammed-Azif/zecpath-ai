"""
Day 28 - AI Screening Report Schema

Defines the structured format used by recruiter-facing
AI screening reports.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScreeningReport:
    candidate_id: str
    candidate_name: str

    screening_status: str = "Review"

    key_answers: dict[str, Any] = field(default_factory=dict)

    confirmed_skills: list[str] = field(default_factory=list)

    salary_expectation: str | None = None
    availability: str | None = None

    strengths: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    missing_data: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate_name": self.candidate_name,
            "screening_status": self.screening_status,
            "key_answers": self.key_answers,
            "confirmed_skills": self.confirmed_skills,
            "salary_expectation": self.salary_expectation,
            "availability": self.availability,
            "strengths": self.strengths,
            "risks": self.risks,
            "missing_data": self.missing_data,
            "metadata": self.metadata,
        }
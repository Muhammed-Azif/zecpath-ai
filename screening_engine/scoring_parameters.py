"""
Day 26 - Screening Scoring Parameters

Defines the scoring weights used to evaluate
candidate screening responses.
"""


SCORING_WEIGHTS = {
    "clarity": 0.25,
    "relevance": 0.30,
    "completeness": 0.25,
    "consistency": 0.20,
}


SCORE_LABELS = {
    "excellent": 85,
    "good": 70,
    "average": 50,
    "poor": 0,
}
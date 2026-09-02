"""
Day 26 - Screening Score Aggregator

Combines multiple question scores into
one final candidate screening score.
"""

from screening_engine.score_normalizer import ScoreNormalizer


class ScreeningAggregator:

    def __init__(self):
        self.normalizer = ScoreNormalizer()

    def aggregate(self, question_scores: list) -> dict:

        if not question_scores:

            return {
                "total_score": 0.0,
                "normalized_score": 0.0,
                "classification": "Needs Improvement",
                "questions_scored": 0,
            }

        total_score = sum(
            item["weighted_score"]
            for item in question_scores
        )

        average_score = (
            total_score
            / len(question_scores)
        )

        normalized_score = self.normalizer.normalize(
            average_score
        )

        classification = (
            self.normalizer.get_label(
                normalized_score
            )
        )

        return {
            "total_score": round(total_score, 2),
            "normalized_score": normalized_score,
            "classification": classification,
            "questions_scored": len(question_scores),
        }
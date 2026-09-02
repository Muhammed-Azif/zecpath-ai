"""
Day 26 - Score Normalizer

Normalizes screening scores into
a standard 0-100 range.
"""


class ScoreNormalizer:

    def normalize(
        self,
        score: float,
        minimum: float = 0.0,
        maximum: float = 100.0
    ) -> float:

        if maximum <= minimum:
            return 0.0

        normalized = (
            (score - minimum)
            / (maximum - minimum)
        ) * 100

        normalized = max(
            0.0,
            min(100.0, normalized)
        )

        return round(normalized, 2)

    def get_label(self, score: float) -> str:

        if score >= 85:
            return "Excellent"

        if score >= 70:
            return "Good"

        if score >= 50:
            return "Average"

        return "Needs Improvement"
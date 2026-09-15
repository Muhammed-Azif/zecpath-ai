"""
Day 27 - Behavioral Indicators Report

Combines confidence and sentiment signals into a
communication-quality report.
"""

from typing import Any, Dict


class BehavioralReportGenerator:
    """Generate a behavioral communication report."""

    def generate(
        self,
        confidence_result: Dict[str, Any],
        sentiment_result: Dict[str, Any],
    ) -> Dict[str, Any]:

        confidence_score = confidence_result.get(
            "confidence_score",
            0,
        )

        confidence_level = confidence_result.get(
            "confidence_level",
            "low",
        )

        sentiment = sentiment_result.get(
            "sentiment",
            "neutral",
        )

        sentiment_score = sentiment_result.get(
            "sentiment_score",
            0,
        )

        strengths = []
        concerns = []

        # Confidence indicators.
        if confidence_score >= 75:
            strengths.append("confident communication")
        elif confidence_score < 50:
            concerns.append("low confidence signals")

        if confidence_result.get("hesitation_count", 0) == 0:
            strengths.append("minimal hesitation")

        if confidence_result.get("uncertainty_count", 0) == 0:
            strengths.append("clear communication")

        if confidence_result.get(
            "contradiction_detected",
            False,
        ):
            concerns.append("possible contradictory response")

        if confidence_result.get(
            "speaking_pace_wpm",
            0,
        ):
            pace = confidence_result["speaking_pace_wpm"]

            if 100 <= pace <= 170:
                strengths.append("balanced speaking pace")
            elif pace < 70:
                concerns.append("slow speaking pace")
            elif pace > 210:
                concerns.append("fast speaking pace")

        # Sentiment indicators.
        if sentiment == "positive":
            strengths.append("positive response sentiment")

        elif sentiment == "negative":
            concerns.append("negative response sentiment")

        # Overall communication assessment.
        overall_score = round(
            (confidence_score + (sentiment_score + 100) / 2) / 2
        )

        if overall_score >= 75:
            overall = "strong"
        elif overall_score >= 50:
            overall = "moderate"
        else:
            overall = "needs_improvement"

        return {
            "communication_strength": overall,
            "overall_score": overall_score,
            "confidence": {
                "score": confidence_score,
                "level": confidence_level,
            },
            "sentiment": {
                "label": sentiment,
                "score": sentiment_score,
            },
            "strength_indicators": strengths,
            "behavioral_concerns": concerns,
        }
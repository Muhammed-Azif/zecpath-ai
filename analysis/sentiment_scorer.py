"""
Day 27 - Sentiment Scoring

Provides lightweight rule-based sentiment analysis
for HR screening answers.
"""

import re
from typing import Any, Dict


class SentimentScorer:
    """Calculate positive, negative and neutral sentiment."""

    POSITIVE_WORDS = {
        "good",
        "great",
        "excellent",
        "happy",
        "excited",
        "confident",
        "successful",
        "success",
        "enjoy",
        "enjoyed",
        "love",
        "like",
        "motivated",
        "interested",
        "passionate",
        "positive",
        "achieved",
        "improved",
        "growth",
        "opportunity",
    }

    NEGATIVE_WORDS = {
        "bad",
        "poor",
        "hate",
        "dislike",
        "difficult",
        "difficulties",
        "problem",
        "problems",
        "failure",
        "failed",
        "worried",
        "confused",
        "frustrated",
        "negative",
        "boring",
        "stress",
        "stressed",
        "unhappy",
        "weak",
    }

    def analyze(self, answer: str) -> Dict[str, Any]:
        """Analyze sentiment of a screening answer."""

        text = answer.strip().lower()

        if not text:
            return {
                "sentiment": "neutral",
                "sentiment_score": 0,
                "positive_count": 0,
                "negative_count": 0,
            }

        words = re.findall(r"\b[\w']+\b", text)

        positive_count = sum(
            1 for word in words if word in self.POSITIVE_WORDS
        )

        negative_count = sum(
            1 for word in words if word in self.NEGATIVE_WORDS
        )

        raw_score = positive_count - negative_count

        if raw_score > 0:
            sentiment = "positive"
        elif raw_score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Normalize sentiment score to -100 .. +100.
        total_signal_words = positive_count + negative_count

        if total_signal_words:
            score = round(
                (raw_score / total_signal_words) * 100
            )
        else:
            score = 0

        return {
            "sentiment": sentiment,
            "sentiment_score": score,
            "positive_count": positive_count,
            "negative_count": negative_count,
        }
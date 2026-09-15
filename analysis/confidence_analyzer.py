"""
Day 27 - Confidence Analysis

Analyzes communication signals from screening answers.

The module detects:
- hesitation patterns
- uncertainty
- response length
- speaking pace
- contradictions
- communication strengths

This is a rule-based signal analysis layer and does not
make psychological or personality diagnoses.
"""

import re
from typing import Any, Dict, List


class ConfidenceAnalyzer:
    """Analyze confidence-related communication signals."""

    HESITATION_PATTERNS = [
        "um",
        "umm",
        "uh",
        "uhh",
        "hmm",
        "maybe",
        "i think",
        "i guess",
        "sort of",
        "kind of",
        "probably",
        "perhaps",
        "not sure",
    ]

    UNCERTAINTY_PATTERNS = [
        "i don't know",
        "i am not sure",
        "i'm not sure",
        "not certain",
        "possibly",
        "might be",
        "could be",
        "i guess",
        "i think",
        "maybe",
    ]

    CONTRADICTION_PATTERNS = [
        "but earlier",
        "actually",
        "however",
        "on the other hand",
        "i said",
        "correction",
    ]

    STRONG_PATTERNS = [
        "i have experience",
        "i successfully",
        "i developed",
        "i implemented",
        "i achieved",
        "i led",
        "i completed",
        "i can",
        "i am confident",
    ]

    def analyze(
        self,
        answer: str,
        duration_seconds: float | None = None,
        previous_answers: List[str] | None = None,
    ) -> Dict[str, Any]:
        """Analyze confidence signals in an answer."""

        text = answer.strip()

        if not text:
            return {
                "confidence_score": 0,
                "confidence_level": "low",
                "word_count": 0,
                "hesitation_count": 0,
                "uncertainty_count": 0,
                "speaking_pace_wpm": 0,
                "contradiction_detected": False,
                "strength_indicators": [],
                "confidence_signals": [],
            }

        normalized = text.lower()
        word_count = len(re.findall(r"\b[\w']+\b", text))

        hesitation_count = self._count_patterns(
            normalized,
            self.HESITATION_PATTERNS,
        )

        uncertainty_count = self._count_patterns(
            normalized,
            self.UNCERTAINTY_PATTERNS,
        )

        contradiction_detected = self._detect_contradiction(
            normalized,
            previous_answers or [],
        )

        strength_indicators = self._find_patterns(
            normalized,
            self.STRONG_PATTERNS,
        )

        pace = self._calculate_pace(
            word_count,
            duration_seconds,
        )

        score = self._calculate_score(
            word_count=word_count,
            hesitation_count=hesitation_count,
            uncertainty_count=uncertainty_count,
            contradiction_detected=contradiction_detected,
            strength_count=len(strength_indicators),
            speaking_pace=pace,
        )

        level = self._confidence_level(score)

        signals = self._build_signals(
            hesitation_count,
            uncertainty_count,
            contradiction_detected,
            strength_indicators,
            pace,
        )

        return {
            "confidence_score": score,
            "confidence_level": level,
            "word_count": word_count,
            "hesitation_count": hesitation_count,
            "uncertainty_count": uncertainty_count,
            "speaking_pace_wpm": pace,
            "contradiction_detected": contradiction_detected,
            "strength_indicators": strength_indicators,
            "confidence_signals": signals,
        }

    @staticmethod
    def _count_patterns(text: str, patterns: List[str]) -> int:
        count = 0

        for pattern in patterns:
            count += len(
                re.findall(
                    r"\b" + re.escape(pattern) + r"\b",
                    text,
                )
            )

        return count

    @staticmethod
    def _find_patterns(text: str, patterns: List[str]) -> List[str]:
        found = []

        for pattern in patterns:
            if re.search(r"\b" + re.escape(pattern) + r"\b", text):
                found.append(pattern)

        return found

    def _detect_contradiction(
        self,
        current_answer: str,
        previous_answers: List[str],
    ) -> bool:

        if self._count_patterns(
            current_answer,
            self.CONTRADICTION_PATTERNS,
        ) > 0:
            return True

        # Basic numeric contradiction detection.
        current_numbers = set(
            re.findall(r"\b\d+(?:\.\d+)?\b", current_answer)
        )

        for previous in previous_answers:
            previous_numbers = set(
                re.findall(
                    r"\b\d+(?:\.\d+)?\b",
                    previous.lower(),
                )
            )

            if current_numbers and previous_numbers:
                if current_numbers.isdisjoint(previous_numbers):
                    return True

        return False

    @staticmethod
    def _calculate_pace(
        word_count: int,
        duration_seconds: float | None,
    ) -> float:

        if not duration_seconds or duration_seconds <= 0:
            return 0

        return round(
            word_count / (duration_seconds / 60),
            2,
        )

    @staticmethod
    def _calculate_score(
        word_count: int,
        hesitation_count: int,
        uncertainty_count: int,
        contradiction_detected: bool,
        strength_count: int,
        speaking_pace: float,
    ) -> int:

        score = 60

        # Useful response length.
        if word_count >= 15:
            score += 10
        elif word_count < 5:
            score -= 15

        # Hesitation penalties.
        score -= min(hesitation_count * 5, 20)

        # Uncertainty penalties.
        score -= min(uncertainty_count * 6, 24)

        # Strong communication indicators.
        score += min(strength_count * 5, 15)

        # Contradiction penalty.
        if contradiction_detected:
            score -= 15

        # Pace signal.
        if speaking_pace:
            if 100 <= speaking_pace <= 170:
                score += 5
            elif speaking_pace < 70 or speaking_pace > 210:
                score -= 5

        return max(0, min(100, score))

    @staticmethod
    def _confidence_level(score: int) -> str:

        if score >= 75:
            return "high"

        if score >= 50:
            return "medium"

        return "low"

    @staticmethod
    def _build_signals(
        hesitation_count: int,
        uncertainty_count: int,
        contradiction_detected: bool,
        strength_indicators: List[str],
        speaking_pace: float,
    ) -> List[str]:

        signals = []

        if hesitation_count:
            signals.append("hesitation_detected")

        if uncertainty_count:
            signals.append("uncertainty_detected")

        if contradiction_detected:
            signals.append("possible_contradiction")

        if strength_indicators:
            signals.append("strong_communication_language")

        if speaking_pace:
            if 100 <= speaking_pace <= 170:
                signals.append("balanced_speaking_pace")
            elif speaking_pace < 70:
                signals.append("slow_speaking_pace")
            elif speaking_pace > 210:
                signals.append("fast_speaking_pace")

        if not signals:
            signals.append("stable_communication")

        return signals
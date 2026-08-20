"""
Day 25 - Candidate Answer Quality Detection
"""

import re


class AnswerQualityDetector:

    VAGUE_PHRASES = [
        "i don't know",
        "not sure",
        "maybe",
        "anything",
        "whatever",
        "somewhere",
        "it depends",
        "i think so",
        "probably",
    ]

    def check(self, answer: str, intent: str) -> dict:

        if not answer or not answer.strip():
            return {
                "quality": "missing",
                "reason": "No answer provided"
            }

        text = answer.strip().lower()

        if len(text) < 3:
            return {
                "quality": "missing",
                "reason": "Answer is too short"
            }

        for phrase in self.VAGUE_PHRASES:
            if phrase in text:
                return {
                    "quality": "vague",
                    "reason": f"Vague phrase detected: {phrase}"
                }

        if intent == "skills":
            if not re.search(
                r"python|java|sql|javascript|machine learning|react|aws|docker|git",
                text
            ):
                return {
                    "quality": "vague",
                    "reason": "No specific skill identified"
                }

        if intent == "experience":
            if not re.search(
                r"\d+\s*(years?|months?)",
                text
            ):
                return {
                    "quality": "vague",
                    "reason": "Experience duration not specified"
                }

        if intent == "salary":
            if not re.search(
                r"\d+(\.\d+)?\s*(lpa|lakhs?|lakh|inr|rs|₹)?",
                text
            ):
                return {
                    "quality": "vague",
                    "reason": "Salary expectation not specified"
                }

        return {
            "quality": "complete",
            "reason": "Answer contains sufficient information"
        }
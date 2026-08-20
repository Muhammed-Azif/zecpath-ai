"""
Day 25 - Candidate Answer Information Extractor
"""

import re


class AnswerExtractor:

    SKILL_PATTERNS = [
        "python",
        "java",
        "javascript",
        "typescript",
        "sql",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "django",
        "flask",
        "react",
        "angular",
        "docker",
        "git",
        "aws",
        "azure",
        "html",
        "css",
    ]

    def extract_skills(self, text: str) -> list:
        text_lower = text.lower()

        found = []

        for skill in self.SKILL_PATTERNS:
            if skill in text_lower:
                found.append(skill)

        return found

    def extract_experience(self, text: str) -> dict:
        text_lower = text.lower()

        years = re.findall(
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            text_lower
        )

        months = re.findall(
            r"(\d+)\s*(?:months?|mos?)",
            text_lower
        )

        return {
            "years": float(years[0]) if years else None,
            "months": int(months[0]) if months else None,
        }

    def extract_salary(self, text: str) -> dict:
        text_lower = text.lower()

        amount = re.findall(
            r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?|lakh)?",
            text_lower
        )

        lpa = None

        if "lpa" in text_lower or "lakh" in text_lower:
            if amount:
                lpa = float(amount[0])

        return {
            "expected_lpa": lpa
        }

    def extract_availability(self, text: str) -> dict:
        text_lower = text.lower()

        immediate = any(
            phrase in text_lower
            for phrase in [
                "immediately",
                "immediate",
                "available now",
                "can join now",
            ]
        )

        return {
            "immediate": immediate,
            "text": text.strip(),
        }

    def extract(self, text: str, intent: str) -> dict:

        if intent == "skills":
            return {
                "skills": self.extract_skills(text)
            }

        if intent == "experience":
            return {
                "experience": self.extract_experience(text)
            }

        if intent == "salary":
            return {
                "salary": self.extract_salary(text)
            }

        if intent == "availability":
            return {
                "availability": self.extract_availability(text)
            }

        return {}
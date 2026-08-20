"""
Day 25 - Answer Intent Classifier

Classifies candidate answers into screening-related intents.
"""

import re


class IntentClassifier:

    INTENTS = [
        "skills",
        "experience",
        "availability",
        "salary",
        "education",
        "location",
        "introduction",
        "notice_period",
        "off_topic",
        "unknown",
    ]

    KEYWORDS = {
        "skills": [
            "skill",
            "skills",
            "python",
            "java",
            "sql",
            "machine learning",
            "deep learning",
            "javascript",
            "react",
            "angular",
            "django",
            "flask",
            "tensorflow",
            "pytorch",
            "aws",
            "docker",
            "git",
        ],

        "experience": [
            "experience",
            "worked",
            "working",
            "years",
            "months",
            "developer",
            "engineer",
            "intern",
            "project",
            "projects",
        ],

        "availability": [
            "available",
            "availability",
            "join",
            "joining",
            "immediately",
            "immediate",
            "start",
            "starting",
        ],

        "salary": [
            "salary",
            "expected",
            "expect",
            "package",
            "lpa",
            "pay",
            "compensation",
            "ctc",
            "lakhs",
            "per annum",
        ],

        "education": [
            "education",
            "degree",
            "btech",
            "b.tech",
            "mtech",
            "m.tech",
            "bachelor",
            "master",
            "college",
            "university",
            "graduation",
            "graduate",
        ],

        "location": [
            "location",
            "located",
            "city",
            "remote",
            "relocate",
            "relocation",
            "kerala",
            "india",
            "trivandrum",
            "bangalore",
            "bengaluru",
            "kochi",
            "chennai",
        ],

        "introduction": [
            "my name",
            "i am",
            "i'm",
            "myself",
            "about me",
            "introduce",
            "introduction",
        ],

        "notice_period": [
            "notice period",
            "notice",
            "days",
            "weeks",
            "serving notice",
            "last working day",
        ],
    }

    def classify(self, answer: str) -> dict:
        """
        Classify a candidate answer.

        Returns:
            {
                "intent": str,
                "confidence": float,
                "matched_keywords": list
            }
        """

        if not answer or not answer.strip():
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "matched_keywords": [],
            }

        text = answer.lower().strip()

        scores = {}

        for intent, keywords in self.KEYWORDS.items():
            matches = []

            for keyword in keywords:
                if keyword in text:
                    matches.append(keyword)

            scores[intent] = matches

        ranked = sorted(
            scores.items(),
            key=lambda item: len(item[1]),
            reverse=True
        )

        best_intent, matches = ranked[0]

        if not matches:
            return {
                "intent": "off_topic",
                "confidence": 0.75,
                "matched_keywords": [],
            }

        total_matches = len(matches)

        if total_matches >= 3:
            confidence = 0.95
        elif total_matches == 2:
            confidence = 0.88
        else:
            confidence = 0.75

        return {
            "intent": best_intent,
            "confidence": confidence,
            "matched_keywords": matches,
        }
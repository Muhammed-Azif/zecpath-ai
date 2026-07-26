"""
Day 9 - Skill Confidence Scorer

Assigns a confidence score to each extracted skill based
on how the skill was detected.
"""


class SkillConfidenceScorer:

    # Confidence values for different detection methods
    SCORES = {
        "exact_match": 1.00,
        "synonym_match": 0.95,
        "skill_stack": 0.95,
        "nlp_match": 0.85,
        "fuzzy_match": 0.80,
    }

    def score(self, detection_method):
        """
        Return confidence score for a detection method.
        """

        return self.SCORES.get(
            detection_method,
            0.50
        )

    def score_skill(
        self,
        skill,
        detection_methods
    ):
        """
        Calculate the final confidence for a skill.

        If a skill is detected using multiple methods,
        the strongest evidence is used.
        """

        if not detection_methods:
            return {
                "skill": skill,
                "confidence": 0.50
            }

        scores = [
            self.score(method)
            for method in detection_methods
        ]

        confidence = max(scores)

        return {
            "skill": skill,
            "confidence": round(confidence, 2)
        }
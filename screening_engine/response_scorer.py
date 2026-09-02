"""
Day 26 - Candidate Response Scorer

Scores individual screening answers based on:

- Clarity
- Relevance
- Completeness
- Consistency
"""

from screening_engine.scoring_parameters import SCORING_WEIGHTS


class ResponseScorer:

    def calculate_clarity(self, answer: str, quality: str) -> float:
        """
        Score how clearly the candidate answered.
        """

        if not answer or not answer.strip():
            return 0.0

        word_count = len(answer.split())

        if quality == "missing":
            return 0.0

        if quality == "vague":
            return 40.0

        if word_count < 3:
            return 35.0

        if word_count < 6:
            return 60.0

        if word_count < 15:
            return 80.0

        return 95.0

    def calculate_relevance(
        self,
        intent: str,
        off_topic: bool
    ) -> float:
        """
        Score whether the answer is relevant
        to the screening context.
        """

        if off_topic:
            return 0.0

        if intent == "unknown":
            return 30.0

        return 100.0

    def calculate_completeness(
        self,
        entities: dict,
        quality: str
    ) -> float:
        """
        Score whether useful information
        was extracted from the answer.
        """

        if quality == "missing":
            return 0.0

        if quality == "vague":
            return 40.0

        if not entities:
            return 50.0

        has_data = False

        for value in entities.values():

            if isinstance(value, list) and len(value) > 0:
                has_data = True

            elif isinstance(value, dict):
                if any(
                    item is not None and item is not False
                    for item in value.values()
                ):
                    has_data = True

        if has_data:
            return 100.0

        return 60.0

    def calculate_consistency(
        self,
        intent: str,
        quality: str,
        off_topic: bool
    ) -> float:
        """
        Score consistency between answer meaning
        and extracted semantic information.
        """

        if off_topic:
            return 0.0

        if quality == "missing":
            return 0.0

        if quality == "vague":
            return 50.0

        if intent == "unknown":
            return 40.0

        return 100.0

    def calculate_score(self, answer_result: dict) -> dict:
        """
        Calculate the complete score for one answer.
        """

        answer = answer_result.get("answer", "")
        intent = answer_result.get("intent", "unknown")
        entities = answer_result.get("entities", {})
        quality = answer_result.get("quality", "missing")
        off_topic = answer_result.get("off_topic", False)

        # A missing answer should receive zero
        # for all screening parameters.
        if quality == "missing" or not answer.strip():

            return {
                "question_id": answer_result.get(
                    "question_id",
                    ""
                ),
                "intent": intent,

                "scores": {
                    "clarity": 0.0,
                    "relevance": 0.0,
                    "completeness": 0.0,
                    "consistency": 0.0,
                },

                "weighted_score": 0.0,

                "quality": quality,
                "off_topic": off_topic,
            }

        clarity = self.calculate_clarity(
            answer,
            quality
        )

        relevance = self.calculate_relevance(
            intent,
            off_topic
        )

        completeness = self.calculate_completeness(
            entities,
            quality
        )

        consistency = self.calculate_consistency(
            intent,
            quality,
            off_topic
        )

        weighted_score = (
            clarity * SCORING_WEIGHTS["clarity"]
            + relevance * SCORING_WEIGHTS["relevance"]
            + completeness * SCORING_WEIGHTS["completeness"]
            + consistency * SCORING_WEIGHTS["consistency"]
        )

        return {
            "question_id": answer_result.get(
                "question_id",
                ""
            ),
            "intent": intent,

            "scores": {
                "clarity": round(clarity, 2),
                "relevance": round(relevance, 2),
                "completeness": round(completeness, 2),
                "consistency": round(consistency, 2),
            },

            "weighted_score": round(
                weighted_score,
                2
            ),

            "quality": quality,
            "off_topic": off_topic,
        }
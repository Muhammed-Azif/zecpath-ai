"""
Day 26 - Screening Score Explainer

Generates human-readable explanations
for screening scores.
"""


class ScreeningScoreExplainer:

    def explain_question(
        self,
        question_score: dict
    ) -> list:

        explanations = []

        scores = question_score.get(
            "scores",
            {}
        )

        if scores.get("clarity", 0) >= 80:
            explanations.append(
                "The response was clear and understandable."
            )
        else:
            explanations.append(
                "The response could be clearer."
            )

        if scores.get("relevance", 0) >= 80:
            explanations.append(
                "The response was relevant to the screening context."
            )
        else:
            explanations.append(
                "The response had low relevance or was off-topic."
            )

        if scores.get("completeness", 0) >= 80:
            explanations.append(
                "The response contained sufficient information."
            )
        else:
            explanations.append(
                "The response may be missing important details."
            )

        if scores.get("consistency", 0) >= 80:
            explanations.append(
                "The response was semantically consistent."
            )
        else:
            explanations.append(
                "The response showed possible inconsistency or vagueness."
            )

        return explanations

    def explain_final_score(
        self,
        aggregate_result: dict
    ) -> str:

        score = aggregate_result.get(
            "normalized_score",
            0
        )

        classification = aggregate_result.get(
            "classification",
            "Needs Improvement"
        )

        return (
            f"Final screening score: {score}/100. "
            f"Candidate performance classification: "
            f"{classification}."
        )
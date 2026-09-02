"""
Day 26 - Screening Scoring Engine

Evaluates candidate screening responses using:

- Clarity
- Relevance
- Completeness
- Consistency
"""

from screening_engine.response_scorer import ResponseScorer
from screening_engine.screening_aggregator import ScreeningAggregator
from screening_engine.score_explainer import ScreeningScoreExplainer


class ScreeningScoringEngine:

    def __init__(self):

        self.response_scorer = ResponseScorer()
        self.aggregator = ScreeningAggregator()
        self.explainer = ScreeningScoreExplainer()

    def score_response(
        self,
        answer_result: dict
    ) -> dict:

        score_result = (
            self.response_scorer.calculate_score(
                answer_result
            )
        )

        explanation = (
            self.explainer.explain_question(
                score_result
            )
        )

        score_result["explanation"] = explanation

        return score_result

    def score_screening(
        self,
        answer_results: list
    ) -> dict:

        question_scores = []

        for answer_result in answer_results:

            score_result = self.score_response(
                answer_result
            )

            question_scores.append(
                score_result
            )

        aggregate_result = (
            self.aggregator.aggregate(
                question_scores
            )
        )

        final_explanation = (
            self.explainer.explain_final_score(
                aggregate_result
            )
        )

        return {
            "question_scores": question_scores,
            "final_screening_score": aggregate_result,
            "final_explanation": final_explanation,
        }
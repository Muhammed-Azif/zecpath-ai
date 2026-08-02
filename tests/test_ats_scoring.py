from ats_engine.ats_scorer import ATSScorer
from ats_engine.score_explainer import ScoreExplainer


def main():

    scorer = ATSScorer("AI/ML Engineer")

    result = scorer.calculate_score(

        skills_score=92,

        experience_score=78,

        education_score=100,

        semantic_score=85

    )

    ScoreExplainer().explain(result)


if __name__ == "__main__":
    main()
"""
Zecpath AI - Day 21
ATS + Eligibility Production Demo

Day 20:
Candidate -> Job -> ATS Score

Day 21:
ATS Score + Job Rules -> Eligibility Decision
"""

from ats_engine.ats_scorer import ATSScorer
from ats_engine.score_explainer import ScoreExplainer

from eligibility.eligibility_engine import EligibilityDecisionEngine


def run_pipeline():

    print("\n" + "=" * 70)
    print("       ZECPATH AI - ATS + ELIGIBILITY PIPELINE")
    print("=" * 70)

    # ---------------------------------------------------------
    # Candidate
    # ---------------------------------------------------------

    candidate = {
        "candidate_id": "cand_001",
        "candidate_name": "Priya Sharma",
        "resume": "priya_sharma_resume.pdf",

        # Eligibility information
        "skills": [
            "Python",
            "Machine Learning",
            "SQL",
            "NLP"
        ],

        "experience_years": 2,

        "location": "Trivandrum",

        "available": True
    }

    # ---------------------------------------------------------
    # Job
    # ---------------------------------------------------------

    job = {
        "job_id": "job_001",
        "role": "AI/ML Engineer",
        "company": "Zecpath AI"
    }

    # ---------------------------------------------------------
    # Day 20 ATS component scores
    # ---------------------------------------------------------

    component_scores = {
        "skills": 88,
        "experience": 82,
        "education": 90,
        "semantic": 86
    }

    print("\nCandidate")
    print("-" * 70)
    print("Candidate ID :", candidate["candidate_id"])
    print("Name         :", candidate["candidate_name"])
    print("Resume       :", candidate["resume"])

    print("\nJob")
    print("-" * 70)
    print("Job ID       :", job["job_id"])
    print("Role         :", job["role"])
    print("Company      :", job["company"])

    # ---------------------------------------------------------
    # Day 20 - ATS Scoring
    # ---------------------------------------------------------

    scorer = ATSScorer(
        role=job["role"]
    )

    ats_result = scorer.calculate_score(
        skills_score=component_scores["skills"],
        experience_score=component_scores["experience"],
        education_score=component_scores["education"],
        semantic_score=component_scores["semantic"]
    )

    # ---------------------------------------------------------
    # ATS explanation
    # ---------------------------------------------------------

    print("\nATS Result")
    print("-" * 70)

    explainer = ScoreExplainer()
    explainer.explain(ats_result)

    print(
        f"\nFinal ATS Score : "
        f"{ats_result['final_score']}"
    )

    # ---------------------------------------------------------
    # Day 21 - Eligibility Decision
    # ---------------------------------------------------------

    engine = EligibilityDecisionEngine(
        role=job["role"]
    )

    eligibility_input = {
        "candidate_id": candidate["candidate_id"],
        "job_id": job["job_id"],

        # Connect Day 20 → Day 21
        "ats_score": ats_result["final_score"],

        "skills": candidate["skills"],
        "experience_years": candidate["experience_years"],
        "location": candidate["location"],
        "available": candidate["available"]
    }

    eligibility_result = engine.evaluate(
        eligibility_input
    )

    # ---------------------------------------------------------
    # Final Eligibility Result
    # ---------------------------------------------------------

    print("\nEligibility Result")
    print("-" * 70)

    print(
        "Candidate       :",
        candidate["candidate_name"]
    )

    print(
        "ATS Score       :",
        eligibility_result["ats_score"]
    )

    print(
        "Decision        :",
        eligibility_result["decision"]
    )

    print("\nMandatory Skills")
    print("-" * 70)

    print(
        "Matched         :",
        ", ".join(
            eligibility_result[
                "matched_mandatory_skills"
            ]
        ) or "None"
    )

    print(
        "Missing         :",
        ", ".join(
            eligibility_result[
                "missing_mandatory_skills"
            ]
        ) or "None"
    )

    print("\nDecision Reasons")
    print("-" * 70)

    for reason in eligibility_result["reasons"]:
        print("-", reason)

    print("\n" + "=" * 70)
    print("       ATS + ELIGIBILITY PIPELINE COMPLETED")
    print("=" * 70)

    return eligibility_result


if __name__ == "__main__":
    run_pipeline()
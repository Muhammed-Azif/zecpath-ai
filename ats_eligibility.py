"""
Zecpath AI - Day 21
ATS + Eligibility Integration

Connects the Day 20 ATS scoring result
to the Day 21 Eligibility Decision Engine.
"""

from eligibility.eligibility_engine import EligibilityDecisionEngine


def evaluate_ats_eligibility(
    ats_result,
    candidate,
    job
):
    """
    Convert Day 20 ATS output into a Day 21
    eligibility decision.
    """

    candidate_data = {
        "candidate_id": candidate["candidate_id"],
        "job_id": job["job_id"],

        # Day 20 ATS final score
        "ats_score": ats_result["final_score"],

        # Candidate eligibility information
        "skills": candidate.get("skills", []),
        "experience_years": candidate.get(
            "experience_years",
            0
        ),
        "location": candidate.get(
            "location",
            ""
        ),
        "available": candidate.get(
            "available",
            False
        )
    }

    engine = EligibilityDecisionEngine(
        role=job["role"]
    )

    return engine.evaluate(candidate_data)
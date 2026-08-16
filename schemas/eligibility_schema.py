"""
Day 21 - Candidate Eligibility Result Schema
"""

ELIGIBILITY_DECISIONS = {
    "ELIGIBLE": "Eligible",
    "REVIEW": "Review",
    "REJECTED": "Rejected"
}


def create_eligibility_result(
    candidate_id,
    job_id,
    role,
    decision,
    ats_score,
    matched_mandatory_skills,
    missing_mandatory_skills,
    experience_years,
    location,
    available,
    reasons,
    warnings=None
):
    """
    Standard structure for eligibility results.
    """

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "role": role,
        "decision": decision,
        "ats_score": ats_score,
        "matched_mandatory_skills": matched_mandatory_skills,
        "missing_mandatory_skills": missing_mandatory_skills,
        "experience_years": experience_years,
        "location": location,
        "available": available,
        "reasons": reasons,
        "warnings": warnings or []
    }
    
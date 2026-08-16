"""
Day 21 - Eligibility Decision Engine Demo
Tests Eligible, Review and Rejected candidates.
"""

from eligibility.eligibility_engine import EligibilityDecisionEngine


def print_result(result):
    print("\n" + "=" * 70)
    print("              ZECPATH AI - ELIGIBILITY RESULT")
    print("=" * 70)

    print("Candidate ID :", result["candidate_id"])
    print("Job ID       :", result["job_id"])
    print("Role         :", result["role"])

    print("\nDecision")
    print("-" * 70)
    print("STATUS       :", result["decision"])

    print("\nCandidate Details")
    print("-" * 70)
    print("ATS Score    :", result["ats_score"])
    print("Experience   :", result["experience_years"], "years")
    print("Location     :", result["location"])
    print("Available    :", result["available"])

    print("\nMandatory Skills")
    print("-" * 70)
    print(
        "Matched      :",
        ", ".join(result["matched_mandatory_skills"])
        or "None"
    )

    print(
        "Missing      :",
        ", ".join(result["missing_mandatory_skills"])
        or "None"
    )

    print("\nReasons")
    print("-" * 70)

    for reason in result["reasons"]:
        print("-", reason)

    if result["warnings"]:
        print("\nWarnings")
        print("-" * 70)

        for warning in result["warnings"]:
            print("-", warning)


def main():

    engine = EligibilityDecisionEngine(
        role="AI/ML Engineer"
    )

    candidates = [

        {
            "candidate_id": "cand_001",
            "job_id": "job_001",
            "ats_score": 82,
            "skills": [
                "Python",
                "Machine Learning",
                "SQL",
                "NLP"
            ],
            "experience_years": 2,
            "location": "Trivandrum",
            "available": True
        },

        {
            "candidate_id": "cand_002",
            "job_id": "job_001",
            "ats_score": 62,
            "skills": [
                "Python",
                "Machine Learning",
                "SQL"
            ],
            "experience_years": 2,
            "location": "Trivandrum",
            "available": True
        },

        {
            "candidate_id": "cand_003",
            "job_id": "job_001",
            "ats_score": 42,
            "skills": [
                "Java",
                "HTML",
                "CSS"
            ],
            "experience_years": 0,
            "location": "Mumbai",
            "available": False
        }
    ]

    for candidate in candidates:

        result = engine.evaluate(candidate)

        print_result(result)


if __name__ == "__main__":
    main()
"""
Zecpath AI - Day 20
ATS Final Production Demo

Demonstrates the complete ATS scoring workflow:
Candidate -> Job -> Component Scores -> ATS Score -> Decision
"""

from ats_engine.ats_scorer import ATSScorer
from ats_engine.score_explainer import ScoreExplainer


def run_ats_demo():
    print("\n" + "=" * 65)
    print("              ZECPATH AI - ATS DEMO")
    print("=" * 65)

    # ---------------------------------------------------------
    # Candidate
    # ---------------------------------------------------------
    candidate = {
        "candidate_id": "cand_001",
        "candidate_name": "Priya Sharma",
        "resume": "priya_sharma_resume.pdf"
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
    # Component scores
    # In production these come from the individual
    # matching/parsing modules.
    # ---------------------------------------------------------
    component_scores = {
        "skills": 88,
        "experience": 82,
        "education": 90,
        "semantic": 86
    }

    print("\nCandidate")
    print("-" * 65)
    print(f"Candidate ID : {candidate['candidate_id']}")
    print(f"Name         : {candidate['candidate_name']}")
    print(f"Resume       : {candidate['resume']}")

    print("\nJob")
    print("-" * 65)
    print(f"Job ID       : {job['job_id']}")
    print(f"Role         : {job['role']}")
    print(f"Company      : {job['company']}")

    print("\nInput Scores")
    print("-" * 65)
    for key, value in component_scores.items():
        print(f"{key.title():20}: {value}%")

    # ---------------------------------------------------------
    # ATS scoring
    # ---------------------------------------------------------
    scorer = ATSScorer(role=job["role"])

    result = scorer.calculate_score(
        skills_score=component_scores["skills"],
        experience_score=component_scores["experience"],
        education_score=component_scores["education"],
        semantic_score=component_scores["semantic"]
    )

    # ---------------------------------------------------------
    # Display explanation
    # ---------------------------------------------------------
    explainer = ScoreExplainer()
    explainer.explain(result)

    # ---------------------------------------------------------
    # Final recruitment decision
    # ---------------------------------------------------------
    if result["final_score"] >= 70:
        decision = "SHORTLIST"
    else:
        decision = "REVIEW / REJECT"

    print("\nFinal Decision")
    print("-" * 65)
    print(f"Candidate : {candidate['candidate_name']}")
    print(f"Decision  : {decision}")

    print("\n" + "=" * 65)
    print("             ATS DEMO COMPLETED")
    print("=" * 65)

    return result


if __name__ == "__main__":
    run_ats_demo()
import json
from ats_engine.ats_scorer import ATSScorer


INPUT_FILE = "data/day20_demo/demo_candidates.json"
OUTPUT_FILE = "data/day20_demo/ats_evaluation_report.json"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    results = []

    for candidate in candidates:
        scorer = ATSScorer(candidate["role"])

        score = scorer.calculate_score(
            skills_score=candidate["skills_score"],
            experience_score=candidate["experience_score"],
            education_score=candidate["education_score"],
            semantic_score=candidate["semantic_score"],
        )

        decision = (
            "SHORTLIST"
            if score["final_score"] >= 70
            else "REJECT"
        )

        results.append({
            "candidate_id": candidate["candidate_id"],
            "candidate_name": candidate["candidate_name"],
            "job_id": candidate["job_id"],
            "role": candidate["role"],
            "final_score": score["final_score"],
            "classification": score["classification"],
            "decision": decision,
            "score_breakdown": score["breakdown"],
        })

    report = {
        "project": "Zecpath AI",
        "report_type": "ATS Evaluation Report",
        "total_candidates": len(results),
        "shortlisted": sum(
            1 for r in results if r["decision"] == "SHORTLIST"
        ),
        "rejected": sum(
            1 for r in results if r["decision"] == "REJECT"
        ),
        "candidates": results,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("=" * 65)
    print("             ZECPATH AI ATS EVALUATION REPORT")
    print("=" * 65)

    for result in results:
        print()
        print(f"Candidate : {result['candidate_name']}")
        print(f"ID        : {result['candidate_id']}")
        print(f"Role      : {result['role']}")
        print(f"ATS Score : {result['final_score']}%")
        print(f"Class     : {result['classification']}")
        print(f"Decision  : {result['decision']}")
        print("-" * 65)

    print()
    print(f"Total Candidates : {report['total_candidates']}")
    print(f"Shortlisted      : {report['shortlisted']}")
    print(f"Rejected         : {report['rejected']}")
    print()
    print(f"Report saved to: {OUTPUT_FILE}")
    print("=" * 65)


if __name__ == "__main__":
    main()
from ats_engine.ats_scorer import ATSScorer

from ranking_engine.candidate_ranker import CandidateRanker
from ranking_engine.shortlist_engine import ShortlistEngine
from ranking_engine.report_generator import ReportGenerator


def main():

    scorer = ATSScorer("AI/ML Engineer")

    raw_candidates = [

        {
            "name": "Muhammed Azif",
            "skills": 95,
            "experience": 84,
            "education": 100,
            "semantic": 91
        },

        {
            "name": "Anjali",
            "skills": 90,
            "experience": 80,
            "education": 95,
            "semantic": 87
        },

        {
            "name": "Rahul",
            "skills": 72,
            "experience": 65,
            "education": 90,
            "semantic": 70
        },

        {
            "name": "Arjun",
            "skills": 60,
            "experience": 55,
            "education": 85,
            "semantic": 58
        }

    ]

    candidates = []

    print("Calculating ATS scores...")

    for person in raw_candidates:

        result = scorer.calculate_score(

            person["skills"],
            person["experience"],
            person["education"],
            person["semantic"]

        )

        candidates.append({

            "name": person["name"],

            **result

        })

    print("Ranking candidates...")

    ranker = CandidateRanker()

    ranked = ranker.rank_candidates(candidates)

    shortlist = ShortlistEngine()

    ranked = shortlist.apply(ranked)

    report = ReportGenerator()

    report.display(ranked)

    report.save_csv(ranked)


if __name__ == "__main__":
    main()
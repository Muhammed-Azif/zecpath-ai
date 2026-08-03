"""
Day 14 - Candidate Ranking Engine
"""


class CandidateRanker:

    def rank_candidates(self, candidates):
        """
        Sort candidates based on Final ATS Score.
        """

        ranked = sorted(
            candidates,
            key=lambda x: x["final_score"],
            reverse=True
        )

        for i, candidate in enumerate(ranked, start=1):
            candidate["rank"] = i

        return ranked
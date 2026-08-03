"""
Day 14 - Candidate Shortlisting Engine
"""


class ShortlistEngine:

    def classify(self, score):

        if score >= 85:
            return "Shortlisted"

        elif score >= 70:
            return "Review"

        return "Rejected"

    def apply(self, candidates):

        for candidate in candidates:
            candidate["status"] = self.classify(
                candidate["final_score"]
            )

        return candidates
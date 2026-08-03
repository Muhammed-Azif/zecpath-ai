"""
Day 14 - Recruiter Report Generator
"""

import csv
import os


class ReportGenerator:

    def display(self, candidates):

        print("\n")
        print("=" * 95)
        print("                    ZECPATH AI RECRUITMENT REPORT")
        print("=" * 95)

        print(
            f"{'Rank':<6}"
            f"{'Candidate':<20}"
            f"{'Skills':<10}"
            f"{'Exp':<10}"
            f"{'Edu':<10}"
            f"{'Semantic':<12}"
            f"{'ATS':<8}"
            f"{'Status'}"
        )

        print("-" * 95)

        shortlisted = 0
        review = 0
        rejected = 0

        for c in candidates:

            print(
                f"{c['rank']:<6}"
                f"{c['name']:<20}"
                f"{c['skills']:<10.2f}"
                f"{c['experience']:<10.2f}"
                f"{c['education']:<10.2f}"
                f"{c['semantic']:<12.2f}"
                f"{c['final_score']:<8.2f}"
                f"{c['status']}"
            )

            if c["status"] == "Shortlisted":
                shortlisted += 1
            elif c["status"] == "Review":
                review += 1
            else:
                rejected += 1

        print("=" * 95)

        print(f"Total Candidates : {len(candidates)}")
        print(f"Shortlisted      : {shortlisted}")
        print(f"Review           : {review}")
        print(f"Rejected         : {rejected}")

        print("=" * 95)

    def save_csv(
            self,
            candidates,
            output_file="outputs/ranked_candidates.csv"
    ):

        os.makedirs("outputs", exist_ok=True)

        with open(output_file, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "Rank",
                "Candidate",
                "Skills",
                "Experience",
                "Education",
                "Semantic",
                "ATS",
                "Status"
            ])

            for c in candidates:

                writer.writerow([
                    c["rank"],
                    c["name"],
                    c["skills"],
                    c["experience"],
                    c["education"],
                    c["semantic"],
                    c["final_score"],
                    c["status"]
                ])

        print("\nReport saved to:", output_file)
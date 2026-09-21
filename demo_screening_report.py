"""
Day 28 - AI Screening Report Demo
"""

import json
from pathlib import Path

from screening_reports.report_builder import ScreeningReportBuilder
from screening_reports.report_formatter import ScreeningReportFormatter


def main():
    answers = {
        "key_answers": {
            "experience": "2 years of experience in Python and ML projects",
            "location": "Trivandrum",
        },
        "confirmed_skills": [
            "Python",
            "Machine Learning",
            "SQL",
        ],
        "salary_expectation": "₹6 LPA",
        "availability": "30 days",
    }

    evaluation = {
        "screening_status": "Review",
        "strengths": [
            "Relevant technical experience",
            "Good machine learning exposure",
            "Clear communication",
        ],
        "risks": [
            "30-day notice period",
        ],
        "missing_data": [],
    }

    builder = ScreeningReportBuilder()

    report = builder.build(
        candidate_id="cand_001",
        candidate_name="Priya Sharma",
        answers=answers,
        evaluation=evaluation,
    )

    formatter = ScreeningReportFormatter()

    text_report = formatter.to_text(report)
    json_report = formatter.to_json(report)

    output_dir = Path("outputs/screening_reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    text_path = output_dir / "sample_candidate_report.txt"
    json_path = output_dir / "sample_candidate_report.json"

    text_path.write_text(text_report, encoding="utf-8")
    json_path.write_text(json_report, encoding="utf-8")

    print(text_report)

    print("\nReports generated:")
    print(f"- {text_path}")
    print(f"- {json_path}")


if __name__ == "__main__":
    main()
"""
Day 28 - AI Screening Report Builder

Transforms structured screening evaluations into
recruiter-friendly screening reports.
"""

from .report_schema import ScreeningReport


class ScreeningReportBuilder:

    def build(
        self,
        candidate_id: str,
        candidate_name: str,
        answers: dict,
        evaluation: dict | None = None,
    ) -> ScreeningReport:

        evaluation = evaluation or {}

        key_answers = answers.get("key_answers", {})
        confirmed_skills = answers.get("confirmed_skills", [])

        salary_expectation = answers.get("salary_expectation")
        availability = answers.get("availability")

        strengths = list(evaluation.get("strengths", []))
        risks = list(evaluation.get("risks", []))
        missing_data = list(evaluation.get("missing_data", []))

        if confirmed_skills:
            strengths.append(
                f"Confirmed skills: {', '.join(confirmed_skills)}"
            )

        if salary_expectation:
            key_answers["salary_expectation"] = salary_expectation
        else:
            missing_data.append("Salary expectation")

        if availability:
            key_answers["availability"] = availability
        else:
            missing_data.append("Availability")

        status = evaluation.get("screening_status", "Review")

        return ScreeningReport(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            screening_status=status,
            key_answers=key_answers,
            confirmed_skills=confirmed_skills,
            salary_expectation=salary_expectation,
            availability=availability,
            strengths=self._unique(strengths),
            risks=self._unique(risks),
            missing_data=self._unique(missing_data),
            metadata={
                "report_version": "1.0",
                "generator": "Zecpath AI",
            },
        )

    @staticmethod
    def _unique(items: list[str]) -> list[str]:
        return list(dict.fromkeys(items))
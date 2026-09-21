from screening_reports.report_builder import ScreeningReportBuilder
from screening_reports.report_formatter import ScreeningReportFormatter


def sample_data():
    answers = {
        "key_answers": {
            "experience": "2 years Python experience"
        },
        "confirmed_skills": [
            "Python",
            "Machine Learning"
        ],
        "salary_expectation": "₹6 LPA",
        "availability": "30 days",
    }

    evaluation = {
        "screening_status": "Review",
        "strengths": [
            "Relevant experience"
        ],
        "risks": [
            "Notice period"
        ],
        "missing_data": []
    }

    return answers, evaluation


def test_report_builder():
    answers, evaluation = sample_data()

    builder = ScreeningReportBuilder()

    report = builder.build(
        candidate_id="cand_001",
        candidate_name="Priya Sharma",
        answers=answers,
        evaluation=evaluation,
    )

    assert report.candidate_id == "cand_001"
    assert report.candidate_name == "Priya Sharma"
    assert report.salary_expectation == "₹6 LPA"
    assert report.availability == "30 days"
    assert "Python" in report.confirmed_skills


def test_missing_salary_and_availability():
    answers = {
        "key_answers": {},
        "confirmed_skills": ["Python"],
    }

    builder = ScreeningReportBuilder()

    report = builder.build(
        candidate_id="cand_002",
        candidate_name="Rahul Verma",
        answers=answers,
        evaluation={},
    )

    assert "Salary expectation" in report.missing_data
    assert "Availability" in report.missing_data


def test_text_formatter():
    answers, evaluation = sample_data()

    builder = ScreeningReportBuilder()

    report = builder.build(
        candidate_id="cand_001",
        candidate_name="Priya Sharma",
        answers=answers,
        evaluation=evaluation,
    )

    formatter = ScreeningReportFormatter()

    text = formatter.to_text(report)

    assert "ZECPATH AI - SCREENING REPORT" in text
    assert "Priya Sharma" in text
    assert "SALARY EXPECTATION" in text
    assert "AVAILABILITY" in text
    assert "STRENGTHS" in text
    assert "RISKS" in text


def test_json_formatter():
    answers, evaluation = sample_data()

    builder = ScreeningReportBuilder()

    report = builder.build(
        candidate_id="cand_001",
        candidate_name="Priya Sharma",
        answers=answers,
        evaluation=evaluation,
    )

    formatter = ScreeningReportFormatter()

    json_output = formatter.to_json(report)

    assert '"candidate_id": "cand_001"' in json_output
    assert '"salary_expectation": "₹6 LPA"' in json_output
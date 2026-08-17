"""
Zecpath AI - Day 22
Tests for HR Screening Question Dataset
"""

import json

from screening_ai.question_category_mapping import (
    get_category_mapping,
    get_category_priority
)

from schemas.hr_question_schema import (
    create_question
)


DATASET_PATH = "data/hr_screening_questions.json"


def load_dataset():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def test_dataset_exists_and_loads():
    dataset = load_dataset()

    assert "questions" in dataset
    assert len(dataset["questions"]) > 0


def test_required_categories_exist():
    dataset = load_dataset()

    required_categories = {
        "Introduction",
        "Education",
        "Experience",
        "Skills",
        "Location",
        "Salary",
        "Notice Period"
    }

    dataset_categories = {
        question["category"]
        for question in dataset["questions"]
    }

    assert required_categories.issubset(
        dataset_categories
    )


def test_question_required_fields():
    dataset = load_dataset()

    required_fields = {
        "question_id",
        "category",
        "question",
        "expected_answer_type",
        "mandatory",
        "scoring_importance",
        "roles"
    }

    for question in dataset["questions"]:
        assert required_fields.issubset(
            question.keys()
        )


def test_answer_types_are_valid():
    dataset = load_dataset()

    valid_types = {
        "text",
        "number",
        "list",
        "location",
        "boolean",
        "salary",
        "duration",
        "date"
    }

    for question in dataset["questions"]:
        assert (
            question["expected_answer_type"]
            in valid_types
        )


def test_scoring_importance_is_valid():
    dataset = load_dataset()

    for question in dataset["questions"]:
        assert 1 <= question["scoring_importance"] <= 5


def test_category_mapping():
    mapping = get_category_mapping()

    assert "Introduction" in mapping
    assert "Education" in mapping
    assert "Experience" in mapping
    assert "Skills" in mapping
    assert "Location" in mapping
    assert "Salary" in mapping
    assert "Notice Period" in mapping


def test_category_priority():
    assert get_category_priority("Skills") == 5
    assert get_category_priority("Experience") == 5
    assert get_category_priority("Education") == 2


def test_create_question_object():
    question = create_question(
        question_id="TEST_001",
        category="Skills",
        question="What are your strongest skills?",
        expected_answer_type="list",
        mandatory=True,
        scoring_importance=5,
        roles=["AI/ML Engineer"]
    )

    assert question["question_id"] == "TEST_001"
    assert question["category"] == "Skills"
    assert question["expected_answer_type"] == "list"
    assert question["mandatory"] is True
    assert question["scoring_importance"] == 5
    assert question["roles"] == ["AI/ML Engineer"]
    assert question["language"] == "en"
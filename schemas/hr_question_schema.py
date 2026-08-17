"""
Zecpath AI - Day 22
AI Conversation-Ready HR Question Schema
"""


EXPECTED_ANSWER_TYPES = {
    "text",
    "number",
    "list",
    "location",
    "boolean",
    "salary",
    "duration",
    "date"
}


def create_question(
    question_id,
    category,
    question,
    expected_answer_type,
    mandatory,
    scoring_importance,
    roles=None,
    language="en"
):
    """
    Create a standardized HR screening question object.
    """

    if expected_answer_type not in EXPECTED_ANSWER_TYPES:
        raise ValueError(
            f"Unsupported answer type: {expected_answer_type}"
        )

    if not 1 <= scoring_importance <= 5:
        raise ValueError(
            "scoring_importance must be between 1 and 5"
        )

    return {
        "question_id": question_id,
        "category": category,
        "question": question,
        "expected_answer_type": expected_answer_type,
        "mandatory": mandatory,
        "scoring_importance": scoring_importance,
        "roles": roles or ["All"],
        "language": language
    }
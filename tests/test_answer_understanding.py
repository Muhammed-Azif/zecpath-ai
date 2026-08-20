from answer_engine.answer_understanding import (
    AnswerUnderstandingEngine
)


def test_skill_intent():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        "I know Python, SQL and machine learning."
    )

    assert result["intent"] == "skills"
    assert "python" in result["entities"]["skills"]
    assert result["off_topic"] is False


def test_experience_extraction():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        "I have 3 years of experience in software development."
    )

    assert result["intent"] == "experience"
    assert result["entities"]["experience"]["years"] == 3.0


def test_salary_extraction():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        "My expected salary is 7 LPA."
    )

    assert result["intent"] == "salary"
    assert result["entities"]["salary"]["expected_lpa"] == 7.0


def test_availability():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        "I can join immediately."
    )

    assert result["intent"] == "availability"
    assert result["entities"]["availability"]["immediate"] is True


def test_vague_answer():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        "I don't know, anything is fine."
    )

    assert result["quality"] == "vague"


def test_off_topic_answer():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        "Yesterday I went to the cinema with my friends."
    )

    assert result["off_topic"] is True


def test_missing_answer():

    engine = AnswerUnderstandingEngine()

    result = engine.understand("")

    assert result["quality"] == "missing"


def test_structured_answer():

    engine = AnswerUnderstandingEngine()

    result = engine.understand(
        "I have 2 years of experience with Python.",
        question="How much experience do you have?",
        question_id="q_exp_001"
    )

    assert result["question_id"] == "q_exp_001"
    assert result["question"] == "How much experience do you have?"
    assert result["answer"] != ""
    assert "intent" in result
    assert "entities" in result
    assert "quality" in result
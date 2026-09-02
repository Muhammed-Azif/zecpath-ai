from screening_engine.response_scorer import ResponseScorer
from screening_engine.score_normalizer import ScoreNormalizer
from screening_engine.screening_aggregator import ScreeningAggregator
from screening_engine.screening_engine import ScreeningScoringEngine


def create_good_answer():
    return {
        "question_id": "q_001",
        "question": "What technical skills do you have?",
        "answer": (
            "I have experience with Python, SQL, "
            "machine learning and Git."
        ),
        "intent": "skills",
        "confidence": 0.95,
        "entities": {
            "skills": [
                "python",
                "sql",
                "machine learning",
                "git"
            ]
        },
        "quality": "complete",
        "quality_reason": "Answer contains sufficient information",
        "off_topic": False,
        "matched_keywords": [
            "python",
            "sql",
            "machine learning",
            "git"
        ],
    }


def create_vague_answer():
    return {
        "question_id": "q_002",
        "question": "What skills do you have?",
        "answer": "I don't know, maybe anything.",
        "intent": "off_topic",
        "confidence": 0.75,
        "entities": {},
        "quality": "vague",
        "quality_reason": "Vague phrase detected",
        "off_topic": True,
        "matched_keywords": [],
    }


# --------------------------------------------------
# RESPONSE SCORER TESTS
# --------------------------------------------------

def test_good_response_score():

    scorer = ResponseScorer()

    result = scorer.calculate_score(
        create_good_answer()
    )

    assert result["weighted_score"] >= 80
    assert result["scores"]["clarity"] >= 80
    assert result["scores"]["relevance"] == 100
    assert result["scores"]["completeness"] == 100
    assert result["scores"]["consistency"] == 100


def test_vague_response_score():

    scorer = ResponseScorer()

    result = scorer.calculate_score(
        create_vague_answer()
    )

    assert result["weighted_score"] < 50
    assert result["scores"]["relevance"] == 0
    assert result["scores"]["consistency"] == 0


def test_off_topic_response_score():

    scorer = ResponseScorer()

    answer = create_good_answer()

    answer["intent"] = "off_topic"
    answer["off_topic"] = True

    result = scorer.calculate_score(answer)

    assert result["scores"]["relevance"] == 0
    assert result["scores"]["consistency"] == 0


def test_missing_response_score():

    scorer = ResponseScorer()

    answer = {
        "question_id": "q_003",
        "answer": "",
        "intent": "unknown",
        "entities": {},
        "quality": "missing",
        "off_topic": False,
    }

    result = scorer.calculate_score(answer)

    assert result["weighted_score"] == 0
    assert result["scores"]["clarity"] == 0
    assert result["scores"]["completeness"] == 0


# --------------------------------------------------
# SCORE NORMALIZER TESTS
# --------------------------------------------------

def test_score_normalization():

    normalizer = ScoreNormalizer()

    assert normalizer.normalize(0) == 0
    assert normalizer.normalize(50) == 50
    assert normalizer.normalize(100) == 100


def test_score_boundaries():

    normalizer = ScoreNormalizer()

    assert normalizer.normalize(-20) == 0
    assert normalizer.normalize(120) == 100


def test_score_classification():

    normalizer = ScoreNormalizer()

    assert normalizer.get_label(90) == "Excellent"
    assert normalizer.get_label(75) == "Good"
    assert normalizer.get_label(60) == "Average"
    assert normalizer.get_label(30) == "Needs Improvement"


# --------------------------------------------------
# AGGREGATOR TESTS
# --------------------------------------------------

def test_aggregate_scores():

    aggregator = ScreeningAggregator()

    question_scores = [
        {"weighted_score": 80},
        {"weighted_score": 90},
        {"weighted_score": 70},
    ]

    result = aggregator.aggregate(question_scores)

    assert result["questions_scored"] == 3
    assert result["normalized_score"] == 80
    assert result["classification"] == "Good"


def test_empty_aggregate():

    aggregator = ScreeningAggregator()

    result = aggregator.aggregate([])

    assert result["questions_scored"] == 0
    assert result["normalized_score"] == 0
    assert result["classification"] == "Needs Improvement"


# --------------------------------------------------
# FULL ENGINE TEST
# --------------------------------------------------

def test_full_screening_engine():

    engine = ScreeningScoringEngine()

    answers = [
        create_good_answer(),
        {
            "question_id": "q_002",
            "answer": (
                "I have 2 years of experience "
                "in software development."
            ),
            "intent": "experience",
            "entities": {
                "experience": {
                    "years": 2.0,
                    "months": None,
                }
            },
            "quality": "complete",
            "off_topic": False,
        },
    ]

    result = engine.score_screening(answers)

    assert "question_scores" in result
    assert "final_screening_score" in result
    assert "final_explanation" in result

    assert len(result["question_scores"]) == 2

    assert (
        result["final_screening_score"]
        ["normalized_score"]
        > 0
    )
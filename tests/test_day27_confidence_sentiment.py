from analysis.confidence_analyzer import ConfidenceAnalyzer
from analysis.sentiment_scorer import SentimentScorer
from analysis.behavioral_report import BehavioralReportGenerator


def test_confident_response():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.analyze(
        "I have experience in Python and machine learning. "
        "I successfully completed several projects and improved "
        "my technical skills."
    )

    assert result["confidence_score"] >= 75
    assert result["confidence_level"] == "high"


def test_hesitation_detection():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.analyze(
        "Um, I think maybe I can work with Python."
    )

    assert result["hesitation_count"] > 0
    assert result["uncertainty_count"] > 0


def test_speaking_pace():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.analyze(
        "I have experience working with Python and machine learning "
        "and I completed multiple projects successfully.",
        duration_seconds=10,
    )

    assert result["speaking_pace_wpm"] > 0


def test_empty_answer():

    analyzer = ConfidenceAnalyzer()

    result = analyzer.analyze("")

    assert result["confidence_score"] == 0
    assert result["confidence_level"] == "low"


def test_positive_sentiment():

    scorer = SentimentScorer()

    result = scorer.analyze(
        "I am excited about this opportunity and very interested "
        "in machine learning."
    )

    assert result["sentiment"] == "positive"
    assert result["sentiment_score"] > 0


def test_negative_sentiment():

    scorer = SentimentScorer()

    result = scorer.analyze(
        "I was frustrated and stressed by the difficult project."
    )

    assert result["sentiment"] == "negative"
    assert result["sentiment_score"] < 0


def test_neutral_sentiment():

    scorer = SentimentScorer()

    result = scorer.analyze(
        "I worked on a Python project for six months."
    )

    assert result["sentiment"] == "neutral"


def test_behavioral_report():

    confidence = ConfidenceAnalyzer()
    sentiment = SentimentScorer()

    confidence_result = confidence.analyze(
        "I successfully completed a Python project and "
        "I am confident about my technical skills."
    )

    sentiment_result = sentiment.analyze(
        "I am excited about this opportunity."
    )

    generator = BehavioralReportGenerator()

    report = generator.generate(
        confidence_result,
        sentiment_result,
    )

    assert "communication_strength" in report
    assert "strength_indicators" in report
    assert "behavioral_concerns" in report
    assert report["overall_score"] >= 0
    assert report["overall_score"] <= 100
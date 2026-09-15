"""
Zecpath AI - Day 27 Demo

Confidence & Sentiment Signal Analysis
"""

from analysis.confidence_analyzer import ConfidenceAnalyzer
from analysis.sentiment_scorer import SentimentScorer
from analysis.behavioral_report import BehavioralReportGenerator


def main():
    print("=" * 65)
    print("          ZECPATH AI - DAY 27 DEMO")
    print("     CONFIDENCE & SENTIMENT SIGNAL ANALYSIS")
    print("=" * 65)

    answer = (
        "I am excited about this opportunity. "
        "I have experience working with Python and machine learning. "
        "I successfully completed several projects and improved "
        "my technical skills."
    )

    print("\nCandidate Answer")
    print("-" * 65)
    print(answer)

    # Confidence analysis
    confidence_analyzer = ConfidenceAnalyzer()

    confidence_result = confidence_analyzer.analyze(
        answer,
        duration_seconds=35,
    )

    # Sentiment analysis
    sentiment_scorer = SentimentScorer()

    sentiment_result = sentiment_scorer.analyze(answer)

    # Behavioral report
    report_generator = BehavioralReportGenerator()

    behavioral_report = report_generator.generate(
        confidence_result,
        sentiment_result,
    )

    print("\nConfidence Analysis")
    print("-" * 65)
    print(
        f"Score       : "
        f"{confidence_result['confidence_score']}/100"
    )
    print(
        f"Level       : "
        f"{confidence_result['confidence_level'].capitalize()}"
    )
    print(
        f"Word Count  : "
        f"{confidence_result['word_count']}"
    )
    print(
        f"Hesitation  : "
        f"{confidence_result['hesitation_count']}"
    )
    print(
        f"Uncertainty : "
        f"{confidence_result['uncertainty_count']}"
    )
    print(
        f"Speaking Pace: "
        f"{confidence_result['speaking_pace_wpm']} WPM"
    )
    print(
        f"Contradiction: "
        f"{confidence_result['contradiction_detected']}"
    )

    print("\nSentiment Analysis")
    print("-" * 65)
    print(
        f"Sentiment    : "
        f"{sentiment_result['sentiment'].capitalize()}"
    )
    print(
        f"Score        : "
        f"{sentiment_result['sentiment_score']}"
    )
    print(
        f"Positive     : "
        f"{sentiment_result['positive_count']}"
    )
    print(
        f"Negative     : "
        f"{sentiment_result['negative_count']}"
    )

    print("\nBehavioral Indicators")
    print("-" * 65)
    print(
        f"Communication Strength : "
        f"{behavioral_report['communication_strength']}"
    )
    print(
        f"Overall Score          : "
        f"{behavioral_report['overall_score']}/100"
    )

    print("\nStrength Indicators")
    print("-" * 65)

    for indicator in behavioral_report["strength_indicators"]:
        print(f"- {indicator}")

    print("\nBehavioral Concerns")
    print("-" * 65)

    concerns = behavioral_report["behavioral_concerns"]

    if concerns:
        for concern in concerns:
            print(f"- {concern}")
    else:
        print("- None")

    print("\n" + "=" * 65)
    print("              DAY 27 ANALYSIS COMPLETE")
    print("=" * 65)


if __name__ == "__main__":
    main()
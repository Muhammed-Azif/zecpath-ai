"""
Zecpath AI - Day 26
Screening Scoring Engine Demo
"""

from processors.answer_processor import AnswerProcessor
from screening_engine.screening_engine import (
    ScreeningScoringEngine
)


def main():

    transcript = {
        "transcript_id": "transcript_002",

        "segments": [
            {
                "question_id": "q_001",
                "question": "What technical skills do you have?",
                "text": (
                    "I have experience with Python, SQL, "
                    "machine learning and Git."
                )
            },

            {
                "question_id": "q_002",
                "question": "How much experience do you have?",
                "text": (
                    "I have 2 years of experience "
                    "in software development."
                )
            },

            {
                "question_id": "q_003",
                "question": "What is your expected salary?",
                "text": (
                    "My expected salary is around 6 LPA."
                )
            },

            {
                "question_id": "q_004",
                "question": "When can you join?",
                "text": (
                    "I can join immediately."
                )
            },

            {
                "question_id": "q_005",
                "question": "What technical skills do you have?",
                "text": (
                    "I don't know, maybe anything."
                )
            }
        ]
    }

    answer_processor = AnswerProcessor()

    answer_results = (
        answer_processor.process_transcript(
            transcript
        )
    )

    scoring_engine = (
        ScreeningScoringEngine()
    )

    result = scoring_engine.score_screening(
        answer_results
    )

    print("=" * 72)
    print("              ZECPATH AI - DAY 26")
    print("              SCREENING SCORING ENGINE")
    print("=" * 72)

    for question_score in result["question_scores"]:

        print("\n" + "-" * 72)

        print(
            "Question ID :",
            question_score["question_id"]
        )

        print(
            "Intent      :",
            question_score["intent"]
        )

        print("\nScore Breakdown")

        for name, score in (
            question_score["scores"].items()
        ):

            print(
                f"{name.capitalize():<15}: "
                f"{score}"
            )

        print(
            "\nQuestion Score :",
            question_score["weighted_score"]
        )

        print("\nExplanation:")

        for explanation in (
            question_score["explanation"]
        ):
            print("-", explanation)

    final_score = (
        result["final_screening_score"]
    )

    print("\n" + "=" * 72)
    print("FINAL SCREENING RESULT")
    print("=" * 72)

    print(
        "Questions Scored :",
        final_score["questions_scored"]
    )

    print(
        "Total Score      :",
        final_score["total_score"]
    )

    print(
        "Normalized Score :",
        final_score["normalized_score"],
        "/100"
    )

    print(
        "Classification   :",
        final_score["classification"]
    )

    print(
        "\nExplanation:",
        result["final_explanation"]
    )


if __name__ == "__main__":
    main()
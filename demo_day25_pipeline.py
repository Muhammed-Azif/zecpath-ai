"""
Zecpath AI - Day 25
Transcript -> Answer Understanding Pipeline
"""

from processors.answer_processor import AnswerProcessor


def main():

    transcript = {
        "transcript_id": "transcript_001",

        "segments": [
            {
                "question_id": "q_skills_001",
                "question": "What technical skills do you have?",
                "text": (
                    "I have experience with Python, SQL, "
                    "machine learning and Git."
                )
            },
            {
                "question_id": "q_exp_001",
                "question": "How much experience do you have?",
                "text": (
                    "I have 2 years of experience in software development."
                )
            },
            {
                "question_id": "q_salary_001",
                "question": "What is your expected salary?",
                "text": "I expect around 6 LPA."
            },
            {
                "question_id": "q_availability_001",
                "question": "When can you join?",
                "text": "I can join immediately."
            }
        ]
    }

    processor = AnswerProcessor()

    results = processor.process_transcript(transcript)

    print("=" * 70)
    print("              ZECPATH AI - DAY 25")
    print("        TRANSCRIPT → ANSWER UNDERSTANDING")
    print("=" * 70)

    print(f"\nTranscript ID: {transcript['transcript_id']}")
    print(f"Answers processed: {len(results)}")

    for result in results:

        print("\n" + "-" * 70)

        print("Question ID :", result["question_id"])
        print("Intent      :", result["intent"])
        print("Confidence  :", result["confidence"])
        print("Entities    :", result["entities"])
        print("Quality     :", result["quality"])
        print("Off-topic   :", result["off_topic"])


if __name__ == "__main__":
    main()
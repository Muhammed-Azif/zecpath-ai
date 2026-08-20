"""
Day 25 - Zecpath AI
Answer Intent & Understanding Demo
"""

from answer_engine.answer_understanding import (
    AnswerUnderstandingEngine
)


def main():

    engine = AnswerUnderstandingEngine()

    test_answers = [
        {
            "question_id": "q_001",
            "question": "What technical skills do you have?",
            "answer": (
                "I have experience with Python, SQL, "
                "machine learning and Git."
            )
        },
        {
            "question_id": "q_002",
            "question": "How many years of experience do you have?",
            "answer": (
                "I have 2 years of experience as a Python developer."
            )
        },
        {
            "question_id": "q_003",
            "question": "What is your expected salary?",
            "answer": "I am expecting around 6 LPA."
        },
        {
            "question_id": "q_004",
            "question": "When can you join?",
            "answer": "I am available immediately."
        },
        {
            "question_id": "q_005",
            "question": "What technical skills do you have?",
            "answer": "I don't know, anything is fine."
        },
        {
            "question_id": "q_006",
            "question": "What technical skills do you have?",
            "answer": "I watched a movie yesterday."
        },
    ]

    print("=" * 70)
    print("              ZECPATH AI - DAY 25 DEMO")
    print("          ANSWER INTENT & UNDERSTANDING ENGINE")
    print("=" * 70)

    for item in test_answers:

        result = engine.understand(
            answer=item["answer"],
            question=item["question"],
            question_id=item["question_id"]
        )

        print("\n" + "-" * 70)
        print(f"Question ID : {result['question_id']}")
        print(f"Question    : {result['question']}")
        print(f"Answer      : {result['answer']}")
        print(f"Intent      : {result['intent']}")
        print(f"Confidence  : {result['confidence']}")
        print(f"Entities    : {result['entities']}")
        print(f"Quality     : {result['quality']}")
        print(f"Off-topic   : {result['off_topic']}")

        if result["quality_reason"]:
            print(f"Reason      : {result['quality_reason']}")


if __name__ == "__main__":
    main()
"""
Zecpath AI - Day 22
HR Screening Dataset Demo
"""

import json

from screening_ai.question_category_mapping import (
    get_category_mapping
)


DATASET_PATH = "data/hr_screening_questions.json"


def main():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        dataset = json.load(file)

    questions = dataset["questions"]
    categories = get_category_mapping()

    print("\n" + "=" * 70)
    print("       ZECPATH AI - HR SCREENING DATASET")
    print("=" * 70)

    print("\nDataset")
    print("-" * 70)
    print("Name       :", dataset["dataset_name"])
    print("Version    :", dataset["version"])
    print("Language   :", dataset["language"])
    print("Questions  :", len(questions))

    print("\nCategories")
    print("-" * 70)

    for category, details in categories.items():
        count = sum(
            1
            for question in questions
            if question["category"] == category
        )

        print(
            f"{category:18} : "
            f"{count} questions "
            f"(priority {details['priority']})"
        )

    print("\nSample AI Conversation Objects")
    print("-" * 70)

    for question in questions[:5]:

        print(
            f"\n[{question['question_id']}]"
        )

        print(
            "Category            :",
            question["category"]
        )

        print(
            "Question            :",
            question["question"]
        )

        print(
            "Expected Answer    :",
            question["expected_answer_type"]
        )

        print(
            "Mandatory           :",
            question["mandatory"]
        )

        print(
            "Scoring Importance  :",
            question["scoring_importance"]
        )

        print(
            "Roles               :",
            ", ".join(question["roles"])
        )

    print("\n" + "=" * 70)
    print("       HR SCREENING DATASET READY")
    print("=" * 70)


if __name__ == "__main__":
    main()
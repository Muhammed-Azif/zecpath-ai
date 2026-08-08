import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "day17" / "test_cases.json"


def load_test_cases():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_skill_match(resume_skills, required_skills):
    resume = {skill.lower() for skill in resume_skills}
    required = {skill.lower() for skill in required_skills}

    if not required:
        return 0.0

    matched = resume.intersection(required)

    return len(matched) / len(required)


def calculate_prediction(case):
    skill_score = calculate_skill_match(
        case["resume_skills"],
        case["required_skills"]
    )

    experience = case["experience_years"]

    # Basic system-level decision threshold.
    # This is deliberately kept separate from the existing ATS scorer.
    if skill_score >= 0.66:
        prediction = True
    else:
        prediction = False

    return prediction, skill_score


def calculate_metrics(results):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for result in results:
        actual = result["expected"]
        predicted = result["predicted"]

        if actual and predicted:
            true_positive += 1
        elif not actual and not predicted:
            true_negative += 1
        elif not actual and predicted:
            false_positive += 1
        elif actual and not predicted:
            false_negative += 1

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0
    )

    accuracy = (
        (true_positive + true_negative) /
        len(results)
        if results
        else 0
    )

    return {
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy
    }


def test_day17_system_testing():
    cases = load_test_cases()

    results = []

    for case in cases:
        predicted, skill_score = calculate_prediction(case)

        results.append({
            "id": case["id"],
            "category": case["category"],
            "profile": case["profile"],
            "role": case["role"],
            "expected": case["expected_shortlist"],
            "predicted": predicted,
            "skill_score": skill_score
        })

    metrics = calculate_metrics(results)

    print("\n===== DAY 17 ATS SYSTEM TEST =====")

    for result in results:
        status = (
            "PASS"
            if result["expected"] == result["predicted"]
            else "MISMATCH"
        )

        print(
            f'{result["id"]} | '
            f'{result["role"]} | '
            f'Expected={result["expected"]} | '
            f'Predicted={result["predicted"]} | '
            f'Score={result["skill_score"]:.2f} | '
            f'{status}'
        )

    print("\n===== METRICS =====")
    print(f'Accuracy : {metrics["accuracy"]:.2%}')
    print(f'Precision: {metrics["precision"]:.2%}')
    print(f'Recall   : {metrics["recall"]:.2%}')

    assert metrics["accuracy"] >= 0.70
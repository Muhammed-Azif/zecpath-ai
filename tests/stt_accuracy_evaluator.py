
"""
Day 24 - STT Accuracy Evaluator

Evaluates speech-to-text output against reference transcripts
using Word Error Rate (WER).
"""

import json
from pathlib import Path

from utils.transcript_normalizer import TranscriptNormalizer


BASE_DIR = Path(__file__).resolve().parents[1]

TEST_CASE_FILE = (
    BASE_DIR
    / "data"
    / "stt_accuracy_test_cases.json"
)


def normalize_words(text):
    """
    Convert text into normalized words for comparison.
    """

    if not text:
        return []

    cleaned = TranscriptNormalizer.normalize(text)

    return cleaned.lower().rstrip(".!?").split()


def calculate_wer(reference, hypothesis):
    """
    Calculate Word Error Rate.

    WER = (Substitutions + Deletions + Insertions) / Reference Words
    """

    ref = normalize_words(reference)
    hyp = normalize_words(hypothesis)

    if not ref:
        return 0.0 if not hyp else 1.0

    rows = len(ref) + 1
    cols = len(hyp) + 1

    matrix = [
        [0] * cols
        for _ in range(rows)
    ]

    for i in range(rows):
        matrix[i][0] = i

    for j in range(cols):
        matrix[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):

            if ref[i - 1] == hyp[j - 1]:
                cost = 0
            else:
                cost = 1

            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost,
            )

    distance = matrix[-1][-1]

    return distance / len(ref)


def evaluate_test_cases():

    with open(
        TEST_CASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        test_cases = json.load(file)

    results = []

    for case in test_cases:

        reference = case["reference"]
        stt_output = case["stt_output"]

        raw_wer = calculate_wer(
            reference,
            stt_output
        )

        cleaned_output = TranscriptNormalizer.normalize(
            stt_output
        )

        cleaned_wer = calculate_wer(
            reference,
            cleaned_output
        )

        results.append(
            {
                "test_id": case["test_id"],
                "condition": case["condition"],
                "reference": reference,
                "stt_output": stt_output,
                "cleaned_output": cleaned_output,
                "raw_wer": round(raw_wer, 4),
                "cleaned_wer": round(cleaned_wer, 4),
            }
        )

    return results


if __name__ == "__main__":

    results = evaluate_test_cases()

    print("=" * 70)
    print("ZECPATH AI - STT ACCURACY EVALUATION")
    print("=" * 70)

    for result in results:

        print()
        print(f"Test ID      : {result['test_id']}")
        print(f"Condition    : {result['condition']}")
        print(f"Raw WER      : {result['raw_wer']:.2%}")
        print(f"Cleaned WER  : {result['cleaned_wer']:.2%}")

    print()
    print("=" * 70)


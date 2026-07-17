"""
tests/test_resume_extraction.py

Day 5 Deliverable: Automated test runs for the Resume Text Extraction Engine.

Runs the extractor against every sample resume in data/sample_resumes/,
checks basic quality gates (non-empty output, no leftover bullet glyphs,
expected keywords present, tables captured), and writes a log to
logs/test_results.log plus cleaned outputs to outputs/extracted/.

Run: python tests/test_resume_extraction.py
Exit code 0 = all checks passed, 1 = one or more failures.
"""

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from parsers.resume_text_extractor import extract_and_process  # noqa: E402

SAMPLE_DIR = ROOT / "data" / "sample_resumes"
OUTPUT_DIR = ROOT / "outputs" / "extracted"
LOG_PATH = ROOT / "logs" / "test_results.log"

# file -> keywords we expect to survive extraction + cleaning
EXPECTATIONS = {
    "priya_sharma_resume.pdf": {
        "must_contain": ["PRIYA SHARMA", "Django", "FastAPI", "Nimbus Systems", "AWS Certified Developer"],
        "must_have_table": True,
    },
    "rahul_verma_resume.docx": {
        "must_contain": ["RAHUL VERMA", "React", "TypeScript", "Bluepeak Digital", "Meta Front-End Developer Certificate"],
        "must_have_table": True,
    },
}

RAW_BULLET_GLYPHS = [ch for ch in ["\u2022", "\u25e6", "\u25aa", "\u2023", "\u25cf", "\u2219", "\u00b7"] if ch]


def run_checks(filename: str, result: dict, expectation: dict) -> list:
    """Return a list of failure messages (empty list = all checks passed)."""
    failures = []
    text = result["cleaned_text"]

    if not text or result["char_count"] < 50:
        failures.append(f"Extracted text too short ({result['char_count']} chars)")

    for keyword in expectation.get("must_contain", []):
        if keyword.lower() not in text.lower():
            failures.append(f"Missing expected keyword: '{keyword}'")

    if expectation.get("must_have_table") and "[TABLE]" not in text:
        failures.append("Expected a [TABLE] block but none was found")

    leftover_glyphs = [g for g in RAW_BULLET_GLYPHS if g in text]
    if leftover_glyphs:
        failures.append(f"Un-normalized bullet glyphs remained: {leftover_glyphs}")

    return failures


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_PATH.parent, exist_ok=True)

    log_lines = [f"=== Resume Text Extraction Engine - Test Run @ {time.ctime()} ==="]
    total, passed = 0, 0

    sample_files = sorted(SAMPLE_DIR.glob("*"))
    if not sample_files:
        print(f"No sample resumes found in {SAMPLE_DIR}. Run generate_sample_resumes.py first.")
        sys.exit(1)

    for file_path in sample_files:
        if file_path.suffix.lower() not in (".pdf", ".docx"):
            continue
        total += 1
        filename = file_path.name
        expectation = EXPECTATIONS.get(filename, {})

        try:
            result = extract_and_process(str(file_path), output_dir=str(OUTPUT_DIR))
            failures = run_checks(filename, result, expectation)
        except Exception as exc:  # noqa: BLE001
            failures = [f"Exception during extraction: {exc}"]
            result = {"char_count": 0}

        status = "PASS" if not failures else "FAIL"
        if status == "PASS":
            passed += 1

        log_lines.append(f"\n[{status}] {filename}")
        log_lines.append(f"  chars_extracted: {result.get('char_count', 0)}")
        if failures:
            for f in failures:
                log_lines.append(f"  - {f}")

    summary = f"\n=== Summary: {passed}/{total} passed ==="
    log_lines.append(summary)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print("\n".join(log_lines))
    print(f"\nLog written to: {LOG_PATH}")
    print(f"Cleaned outputs written to: {OUTPUT_DIR}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

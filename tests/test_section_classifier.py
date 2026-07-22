"""
tests/test_section_classifier.py

Day 8 Deliverable: Automated test runs for Resume Section Segmentation.

Pipeline tested: Day 5 (extract + clean) -> Day 8 (segment into sections)

Runs against every sample resume, checks that expected sections were found
and that key content landed in the right section (not misfiled), and writes
a log to logs/test_results.log plus segmented JSON to outputs/segmented/.

Run: python tests/test_section_classifier.py
Exit code 0 = all checks passed, 1 = one or more failures.
"""

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from parsers.resume_text_extractor import extract_and_process  # noqa: E402
from parsers.section_classifier import segment_resume  # noqa: E402

SAMPLE_DIR = ROOT / "data" / "sample_resumes"
OUTPUT_DIR = ROOT / "outputs" / "segmented"
LOG_PATH = ROOT / "logs" / "test_results.log"

# For each sample, which sections must exist, and a snippet expected
# to land specifically inside a given section (catches mis-filing).
EXPECTATIONS = {
    "priya_sharma_resume.pdf": {
        "must_have_sections": ["Header", "Summary", "Skills", "Work Experience", "Education", "Certifications"],
        "content_in_section": {
            "Skills": ["Django", "FastAPI"],
            "Work Experience": ["Nimbus Systems"],
            "Education": ["RV College"],
            "Certifications": ["AWS Certified Developer"],
        },
    },
    "rahul_verma_resume.docx": {
        "must_have_sections": ["Header", "Skills", "Work Experience", "Education", "Certifications"],
        "content_in_section": {
            "Skills": ["React", "TypeScript"],
            "Work Experience": ["Bluepeak Digital"],
            "Education": ["Pune Institute"],
        },
    },
}


def run_checks(result: dict, expectation: dict) -> list:
    failures = []
    sections = result["sections"]

    for expected_section in expectation["must_have_sections"]:
        if expected_section not in sections:
            failures.append(f"Missing expected section: '{expected_section}'")

    for section_name, expected_snippets in expectation["content_in_section"].items():
        section_text = sections.get(section_name, "")
        for snippet in expected_snippets:
            if snippet.lower() not in section_text.lower():
                failures.append(f"Expected '{snippet}' inside section '{section_name}' but it wasn't found there")

    return failures


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_PATH.parent, exist_ok=True)

    log_lines = [f"=== Resume Section Segmentation - Test Run @ {time.ctime()} ==="]
    total, passed = 0, 0

    sample_files = sorted(SAMPLE_DIR.glob("*"))
    sample_files = [f for f in sample_files if f.suffix.lower() in (".pdf", ".docx")]

    if not sample_files:
        print(f"No sample resumes found in {SAMPLE_DIR}.")
        sys.exit(1)

    for file_path in sample_files:
        total += 1
        filename = file_path.name
        expectation = EXPECTATIONS.get(filename, {})

        try:
            extracted = extract_and_process(str(file_path))
            result = segment_resume(
                extracted["cleaned_text"], source_name=filename, output_dir=str(OUTPUT_DIR)
            )
            failures = run_checks(result, expectation) if expectation else []
        except Exception as exc:  # noqa: BLE001
            failures = [f"Exception during segmentation: {exc}"]
            result = {"sections_found": []}

        status = "PASS" if not failures else "FAIL"
        if status == "PASS":
            passed += 1

        log_lines.append(f"\n[{status}] {filename}")
        log_lines.append(f"  sections_found: {result.get('sections_found')}")
        if failures:
            for f_msg in failures:
                log_lines.append(f"  - {f_msg}")

    accuracy = (passed / total * 100) if total else 0
    summary = f"\n=== Summary: {passed}/{total} passed ({accuracy:.1f}% section detection accuracy) ==="
    log_lines.append(summary)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print("\n".join(log_lines))
    print(f"\nLog written to: {LOG_PATH}")
    print(f"Segmented outputs written to: {OUTPUT_DIR}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

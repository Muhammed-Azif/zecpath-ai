"""
tests/test_jd_parser.py

Day 6 Deliverable: Automated test runs for the JD Parsing System.

Runs the parser against every sample JD in data/sample_jds/, checks that
role category, skills, experience range, and education were extracted
correctly, and writes a log to logs/test_results.log plus structured JSON
outputs to outputs/parsed/.

Run: python tests/test_jd_parser.py
Exit code 0 = all checks passed, 1 = one or more failures.
"""

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from parsers.jd_parser import parse_jd  # noqa: E402

SAMPLE_DIR = ROOT / "data" / "sample_jds"
OUTPUT_DIR = ROOT / "outputs" / "parsed"
LOG_PATH = ROOT / "logs" / "test_results.log"

EXPECTATIONS = {
    "mern_stack_developer.txt": {
        "role_category": "Software Engineer - Full Stack",
        "must_have_skills": ["React", "Node.js", "Express.js", "MongoDB", "REST API", "Git"],
        "min_years": 2,
        "max_years": 4,
        "must_have_education": ["b.tech"],
    },
    "ui_ux_designer.txt": {
        "role_category": "Design - UI/UX",
        "must_have_skills": ["Figma", "Adobe XD", "Wireframing", "Prototyping"],
        "min_years": 3,
        "max_years": None,
        "must_have_education": [],  # "Any Graduate" isn't a specific degree keyword
    },
    "sales_executive.txt": {
        "role_category": "Sales",
        "must_have_skills": ["Negotiation", "Cold Calling", "CRM Software", "Excel"],
        "min_years": 0,
        "max_years": 1,
        "must_have_education": [],
    },
}


def run_checks(result: dict, expectation: dict) -> list:
    failures = []

    if result["role_category"] != expectation["role_category"]:
        failures.append(
            f"role_category mismatch: got '{result['role_category']}', expected '{expectation['role_category']}'"
        )

    missing_skills = [s for s in expectation["must_have_skills"] if s not in result["required_skills"]]
    if missing_skills:
        failures.append(f"Missing expected skills: {missing_skills}")

    exp = result["experience_requirement"]
    if exp.get("min_years") != expectation["min_years"]:
        failures.append(f"min_years mismatch: got {exp.get('min_years')}, expected {expectation['min_years']}")
    if exp.get("max_years") != expectation["max_years"]:
        failures.append(f"max_years mismatch: got {exp.get('max_years')}, expected {expectation['max_years']}")

    for kw in expectation["must_have_education"]:
        if kw not in result["education_requirements"]:
            failures.append(f"Missing expected education keyword: '{kw}'")

    return failures


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_PATH.parent, exist_ok=True)

    log_lines = [f"=== JD Parsing System - Test Run @ {time.ctime()} ==="]
    total, passed = 0, 0

    sample_files = sorted(SAMPLE_DIR.glob("*.txt"))
    if not sample_files:
        print(f"No sample JDs found in {SAMPLE_DIR}.")
        sys.exit(1)

    for file_path in sample_files:
        total += 1
        filename = file_path.name
        expectation = EXPECTATIONS.get(filename, {})

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            result = parse_jd(content, source_name=filename, output_dir=str(OUTPUT_DIR))
            failures = run_checks(result, expectation) if expectation else []
        except Exception as exc:  # noqa: BLE001
            failures = [f"Exception during parsing: {exc}"]
            result = {"role_category": "N/A", "required_skills": []}

        status = "PASS" if not failures else "FAIL"
        if status == "PASS":
            passed += 1

        log_lines.append(f"\n[{status}] {filename}")
        log_lines.append(f"  role_category: {result.get('role_category')}")
        log_lines.append(f"  required_skills: {result.get('required_skills')}")
        if failures:
            for f_msg in failures:
                log_lines.append(f"  - {f_msg}")

    summary = f"\n=== Summary: {passed}/{total} passed ==="
    log_lines.append(summary)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print("\n".join(log_lines))
    print(f"\nLog written to: {LOG_PATH}")
    print(f"Parsed JD outputs written to: {OUTPUT_DIR}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

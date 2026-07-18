"""
parsers/jd_parser.py

Day 6 Deliverable: Job Description Parsing System

Converts a raw job description (plain text) into a structured,
AI-readable job requirement object: role category, required skills
(synonym-normalized), experience range, and education preference.

Public API:
    parse_jd(raw_text, output_dir=None, source_name=None) -> dict
"""

import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.text_cleaner import clean_text  # noqa: E402
from utils.skill_synonyms import normalize_skill, normalize_role, known_skill_phrases  # noqa: E402

_KNOWN_SKILL_PHRASES = known_skill_phrases()

# --- Experience requirement patterns -----------------------------------

_EXPERIENCE_PATTERNS = [
    # "3-5 years", "3 - 5 years", "3 to 5 years"
    re.compile(r"(\d+)\s*(?:-|to)\s*(\d+)\s*\+?\s*years?", re.IGNORECASE),
    # "at least 2 years", "minimum 2 years", "2+ years"
    re.compile(r"(?:at least|minimum of|minimum|min\.?)\s*(\d+)\s*\+?\s*years?", re.IGNORECASE),
    re.compile(r"(\d+)\s*\+\s*years?", re.IGNORECASE),
    # "0-1 years", "fresher", "entry level"
    re.compile(r"\bfresher(s)?\b", re.IGNORECASE),
    re.compile(r"\bentry[- ]level\b", re.IGNORECASE),
]

_EDUCATION_KEYWORDS = [
    "b.tech", "btech", "b.e.", "be ", "bachelor's degree", "bachelors degree",
    "bachelor of", "m.tech", "mtech", "m.e.", "master's degree", "masters degree",
    "master of", "mba", "bca", "mca", "b.sc", "bsc", "m.sc", "msc",
    "any graduate", "graduate degree", "diploma", "12th pass", "high school diploma",
    "phd", "ph.d",
]

_ROLE_TITLE_HINT_RE = re.compile(
    r"(?:job title|role|position)\s*[:\-]\s*(.+)", re.IGNORECASE
)


class JobDescriptionParser:
    """Parses raw JD text into a structured job requirement object."""

    # ---- Section-ish extraction helpers -----------------------------------

    def _extract_role_title(self, text: str, first_line: str) -> str:
        match = _ROLE_TITLE_HINT_RE.search(text)
        if match:
            return match.group(1).strip().splitlines()[0].strip()
        # fall back to the first non-empty line of the JD (common convention:
        # the job title is the document's first line / heading)
        return first_line.strip()

    def _extract_experience(self, text: str) -> dict:
        for pattern in _EXPERIENCE_PATTERNS:
            match = pattern.search(text)
            if not match:
                continue
            groups = match.groups()
            if len(groups) == 2 and groups[0] and groups[1]:
                return {"min_years": int(groups[0]), "max_years": int(groups[1]), "raw_match": match.group(0)}
            if len(groups) >= 1 and groups[0] and groups[0].isdigit():
                return {"min_years": int(groups[0]), "max_years": None, "raw_match": match.group(0)}
            # fresher / entry-level style matches
            return {"min_years": 0, "max_years": 1, "raw_match": match.group(0)}
        return {"min_years": None, "max_years": None, "raw_match": None}

    def _extract_education(self, text: str) -> list:
        lower = text.lower()
        found = []
        for kw in _EDUCATION_KEYWORDS:
            if kw in lower and kw.strip() not in found:
                found.append(kw.strip())
        # de-duplicate near-identical abbreviations (e.g. "b.tech" and "btech")
        return sorted(set(found))

    def _extract_skills(self, text: str) -> list:
        lower = text.lower()
        found_canonical = set()
        for phrase in _KNOWN_SKILL_PHRASES:
            # Word-boundary match so short tokens like "js" don't match inside
            # compound terms like "react.js" / "node.js" / "express.js" — '.'
            # and '/' count as word characters here, not boundaries.
            pattern = r"(?<![a-z0-9./])" + re.escape(phrase) + r"(?![a-z0-9./])"
            if re.search(pattern, lower):
                found_canonical.add(normalize_skill(phrase))
        return sorted(found_canonical)

    # ---- Public entry point ------------------------------------------------

    def parse(self, raw_text: str, source_name: str = None, output_dir: str = None) -> dict:
        cleaned = clean_text(raw_text)
        lines = [l for l in cleaned.split("\n") if l.strip()]
        first_line = lines[0] if lines else ""

        role_title_raw = self._extract_role_title(cleaned, first_line)
        role_category = normalize_role(role_title_raw)
        skills = self._extract_skills(cleaned)
        experience = self._extract_experience(cleaned)
        education = self._extract_education(cleaned)

        result = {
            "source_name": source_name or "unnamed_jd",
            "parsed_at": time.time(),
            "role_title_raw": role_title_raw,
            "role_category": role_category,
            "required_skills": skills,
            "experience_requirement": experience,
            "education_requirements": education,
            "char_count": len(cleaned),
            "cleaned_text": cleaned,
            "output_path": None,
        }

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            stem = Path(source_name).stem if source_name else f"jd_{int(time.time())}"
            out_path = os.path.join(output_dir, f"{stem}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            result["output_path"] = out_path

        return result


def parse_jd(raw_text: str, source_name: str = None, output_dir: str = None) -> dict:
    """Module-level convenience wrapper (functional API)."""
    return JobDescriptionParser().parse(raw_text, source_name=source_name, output_dir=output_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python jd_parser.py <jd_text_file> [output_dir]")
        sys.exit(1)
    jd_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs/parsed"
    with open(jd_path, "r", encoding="utf-8") as f:
        content = f.read()
    res = parse_jd(content, source_name=os.path.basename(jd_path), output_dir=out_dir)
    print(json.dumps({k: v for k, v in res.items() if k != "cleaned_text"}, indent=2))

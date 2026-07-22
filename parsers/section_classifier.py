"""
parsers/section_classifier.py

Day 8 Deliverable: Resume Section Segmentation

Takes the cleaned resume text (Day 5 output) and splits it into labeled
sections: Skills, Work Experience, Education, Certifications, Projects,
Summary. Downstream modules (Day 9 Skill Extraction, Day 10 Experience
Parsing, Day 11 Education Parsing) each read from the relevant section
instead of scanning the entire resume — this is far more accurate and
much faster.

Approach: rule-based heading detection (keyword + formatting heuristics)
combined with NLP-lite signals (line length, capitalization, position).
A full ML classifier is possible later, but a well-tuned rule-based system
is the right starting point — transparent, debuggable, and no training
data required.

Public API:
    segment_resume(cleaned_text, output_dir=None, source_name=None) -> dict
"""

import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


# ----------------------------------------------------------------------
# Canonical section names and the heading phrases that map to each one.
# Longest/most-specific phrases are matched first to avoid false positives
# (e.g. "work experience" should win over a bare "experience").
# ----------------------------------------------------------------------
SECTION_HEADING_MAP = {
    "Summary": [
        "summary", "professional summary", "objective", "career objective",
        "profile", "about me",
    ],
    "Skills": [
        "skills", "technical skills", "core skills", "key skills",
        "skills & tools", "technologies",
    ],
    "Work Experience": [
        "work experience", "professional experience", "experience",
        "employment history", "work history",
    ],
    "Education": [
        "education", "academic background", "educational qualifications",
        "qualifications",
    ],
    "Certifications": [
        "certifications", "certification", "licenses & certifications",
        "courses & certifications",
    ],
    "Projects": [
        "projects", "personal projects", "academic projects", "key projects",
    ],
    "Achievements": [
        "achievements", "awards", "honors", "awards & achievements",
    ],
    "Languages": [
        "languages", "language proficiency",
    ],
    "Contact": [
        "contact", "contact information", "personal details", "contact info",
    ],
}

# Build a flat, longest-first lookup: heading phrase -> canonical section
_HEADING_LOOKUP = []
for canonical, phrases in SECTION_HEADING_MAP.items():
    for phrase in phrases:
        _HEADING_LOOKUP.append((phrase, canonical))
_HEADING_LOOKUP.sort(key=lambda pair: len(pair[0]), reverse=True)


class ResumeSectionClassifier:
    """Splits cleaned resume text into labeled sections."""

    def _looks_like_heading(self, line: str) -> bool:
        """
        A line is a heading CANDIDATE if it's short, has no sentence-ending
        punctuation, and is either ALL CAPS, Title Case, or ends with ':'.
        This filters out normal sentences before we even try to match
        against the known heading phrases.
        """
        stripped = line.strip()
        if not stripped or len(stripped) > 45:
            return False
        if stripped.endswith((".", ",", ";")):
            return False
        word_count = len(stripped.split())
        if word_count > 5:
            return False

        is_all_caps = stripped.isupper()
        is_title_case = stripped.istitle()
        ends_with_colon = stripped.endswith(":")

        return is_all_caps or is_title_case or ends_with_colon

    def _match_heading(self, line: str) -> str:
        """Return the canonical section name if this line matches a known
        heading phrase, else None."""
        cleaned = line.strip().rstrip(":").lower()
        for phrase, canonical in _HEADING_LOOKUP:
            if cleaned == phrase:
                return canonical
        return None

    def segment(self, cleaned_text: str) -> dict:
        """
        Walk the resume line by line. Whenever a line looks like a heading
        AND matches a known section phrase, start a new section. Everything
        until the next recognized heading belongs to that section.

        Lines before the first recognized heading go into "Header" (name,
        contact info, etc. — not a formal section but still useful data).
        """
        lines = cleaned_text.split("\n")

        sections = {"Header": []}
        current_section = "Header"

        for line in lines:
            if self._looks_like_heading(line):
                matched = self._match_heading(line)
                if matched:
                    current_section = matched
                    sections.setdefault(current_section, [])
                    continue  # heading line itself isn't content
            sections.setdefault(current_section, [])
            if line.strip():
                sections[current_section].append(line)

        # Join each section's lines back into a block of text
        return {name: "\n".join(content_lines).strip()
                for name, content_lines in sections.items() if content_lines}

    def segment_and_process(self, cleaned_text: str, source_name: str = None,
                             output_dir: str = None) -> dict:
        sections = self.segment(cleaned_text)

        result = {
            "source_name": source_name or "unnamed_resume",
            "segmented_at": time.time(),
            "sections_found": sorted(sections.keys()),
            "sections": sections,
        }

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            stem = Path(source_name).stem if source_name else f"resume_{int(time.time())}"
            out_path = os.path.join(output_dir, f"{stem}_sections.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            result["output_path"] = out_path

        return result


def segment_resume(cleaned_text: str, source_name: str = None, output_dir: str = None) -> dict:
    """Module-level convenience wrapper (functional API)."""
    return ResumeSectionClassifier().segment_and_process(cleaned_text, source_name, output_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python section_classifier.py <cleaned_resume_text_file> [output_dir]")
        sys.exit(1)
    text_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs/segmented"
    with open(text_path, "r", encoding="utf-8") as f:
        content = f.read()
    res = segment_resume(content, source_name=os.path.basename(text_path), output_dir=out_dir)
    print(f"Found sections: {res['sections_found']}")
    print(f"Saved to: {res.get('output_path')}")

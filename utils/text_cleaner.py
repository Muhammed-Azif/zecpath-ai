"""
utils/text_cleaner.py

Text cleaning & normalization helpers for the Resume Text Extraction Engine (Day 5).

These functions are deliberately kept independent of any PDF/DOCX library so
they can be reused by other parsers later in the roadmap (JD parser, section
segmentation, etc.).
"""

import re
import unicodedata

# Characters that commonly show up as "noise" when resumes are exported from
# design tools, scanned, or copy-pasted from PDFs (bullet glyphs, private-use
# icons from icon fonts, stray control characters, etc.)
_BULLET_CHARS = [ch for ch in ["•", "◦", "▪", "‣", "●", "∙", "·", "*"] if ch]
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
_MULTI_BLANK_LINE_RE = re.compile(r"\n{3,}")
_NON_PRINTABLE_ICON_RE = re.compile(r"[\uE000-\uF8FF]")  # Private Use Area (icon fonts)


def remove_control_and_icon_noise(text: str) -> str:
    """Strip control characters and icon-font glyphs that aren't real content."""
    text = _CONTROL_CHAR_RE.sub("", text)
    text = _NON_PRINTABLE_ICON_RE.sub("", text)
    return text


def normalize_unicode(text: str) -> str:
    """Normalize unicode (e.g. combining accents, fancy quotes) to a consistent form."""
    text = unicodedata.normalize("NFKC", text)
    # Normalize "smart" punctuation to plain ASCII equivalents
    replacements = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u2026": "...",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def normalize_bullets(text: str) -> str:
    """Convert every bullet glyph variant to a single canonical '- ' marker."""
    for ch in _BULLET_CHARS:
        text = text.replace(ch, "-")
    # Collapse "- -" style double markers that can appear after the swap above
    text = re.sub(r"^-\s*-\s*", "- ", text, flags=re.MULTILINE)
    return text


def normalize_whitespace(text: str) -> str:
    """Collapse repeated spaces/tabs and excessive blank lines; trim line edges."""
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = _MULTI_SPACE_RE.sub(" ", text)
    text = _MULTI_BLANK_LINE_RE.sub("\n\n", text)
    return text.strip()


def normalize_heading_casing(line: str) -> str:
    """
    Normalize likely section headings (e.g. 'SKILLS', 'work EXPERIENCE') to
    Title Case so downstream section-detection (Day 8) sees a consistent format.
    A line is treated as a heading candidate if it's short, has no trailing
    punctuation, and is mostly uppercase or a known heading keyword.
    """
    known_headings = {
        "skills", "work experience", "experience", "education",
        "certifications", "certification", "projects", "summary",
        "objective", "profile", "achievements", "languages",
        "contact", "contact information", "personal details",
    }
    stripped = line.strip()
    if not stripped or len(stripped) > 40:
        return line
    if stripped == "[TABLE]":  # structural marker inserted by the extractor, not resume content
        return line

    lower = stripped.lower().rstrip(":")
    is_all_caps = stripped.isupper() and len(stripped.split()) <= 4
    is_known = lower in known_headings

    if is_all_caps or is_known:
        return stripped.rstrip(":").title()
    return line


def normalize_headings(text: str) -> str:
    return "\n".join(normalize_heading_casing(line) for line in text.split("\n"))


def clean_text(raw_text: str) -> str:
    """Full cleaning pass: remove noise, normalize unicode, collapse whitespace."""
    text = remove_control_and_icon_noise(raw_text)
    text = normalize_unicode(text)
    text = normalize_whitespace(text)
    return text


def normalize_text(cleaned_text: str) -> str:
    """Full normalization pass: bullets + heading casing, on already-cleaned text."""
    text = normalize_bullets(cleaned_text)
    text = normalize_headings(text)
    text = normalize_whitespace(text)
    return text

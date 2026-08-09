"""
utils/text_cleaner.py

Text cleaning & normalization helpers for the Resume Text Extraction Engine.

Day 18 enhancements:
- Faster compiled regex usage
- Better noisy resume handling
- Line-ending normalization
- Safer empty/non-string input handling
- Repeated punctuation cleanup
- Preserves the existing Day 5 API
"""

import re
import unicodedata


# ---------------------------------------------------------------------------
# Constants / Pre-compiled Regular Expressions
# ---------------------------------------------------------------------------

_BULLET_CHARS = [
    ch
    for ch in ["•", "◦", "▪", "‣", "●", "∙", "·", "*"]
    if ch
]

_CONTROL_CHAR_RE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"
)

_NON_PRINTABLE_ICON_RE = re.compile(
    r"[\uE000-\uF8FF]"
)

_MULTI_SPACE_RE = re.compile(
    r"[ \t]{2,}"
)

_MULTI_BLANK_LINE_RE = re.compile(
    r"\n{3,}"
)

_REPEATED_DASH_RE = re.compile(
    r"(?m)^\s*-\s*-\s*"
)

_REPEATED_PUNCTUATION_RE = re.compile(
    r"([!?,:;])\1{2,}"
)

_TRAILING_SPACE_RE = re.compile(
    r"[ \t]+$",
    re.MULTILINE
)


# ---------------------------------------------------------------------------
# Input Safety
# ---------------------------------------------------------------------------

def _ensure_text(text: str) -> str:
    """
    Safely convert input to text.

    None or empty values return an empty string.
    """
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    return text


# ---------------------------------------------------------------------------
# Noise Removal
# ---------------------------------------------------------------------------

def remove_control_and_icon_noise(text: str) -> str:
    """
    Strip control characters and icon-font glyphs that aren't real content.
    """
    text = _ensure_text(text)

    text = _CONTROL_CHAR_RE.sub("", text)
    text = _NON_PRINTABLE_ICON_RE.sub("", text)

    return text


# ---------------------------------------------------------------------------
# Unicode Normalization
# ---------------------------------------------------------------------------

def normalize_unicode(text: str) -> str:
    """
    Normalize unicode and convert common smart punctuation
    to consistent ASCII equivalents.
    """
    text = _ensure_text(text)

    text = unicodedata.normalize("NFKC", text)

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",  # Non-breaking space
    }

    for src, dst in replacements.items():
        text = text.replace(src, dst)

    return text


# ---------------------------------------------------------------------------
# Bullet Normalization
# ---------------------------------------------------------------------------

def normalize_bullets(text: str) -> str:
    """
    Convert common bullet glyph variants into a canonical '- ' marker.
    """
    text = _ensure_text(text)

    for ch in _BULLET_CHARS:
        text = text.replace(ch, "-")

    # Avoid repeated bullet markers such as:
    # - - Python
    # -- Python
    text = _REPEATED_DASH_RE.sub("- ", text)

    return text


# ---------------------------------------------------------------------------
# Whitespace Normalization
# ---------------------------------------------------------------------------

def normalize_whitespace(text: str) -> str:
    """
    Collapse repeated spaces/tabs and excessive blank lines.
    Also normalizes Windows/Mac line endings.
    """
    text = _ensure_text(text)

    if not text:
        return ""

    # Normalize all line endings first.
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove trailing spaces from every line.
    text = _TRAILING_SPACE_RE.sub("", text)

    # Remove leading/trailing whitespace from each line.
    lines = [line.strip() for line in text.split("\n")]

    text = "\n".join(lines)

    # Collapse repeated spaces/tabs.
    text = _MULTI_SPACE_RE.sub(" ", text)

    # Collapse excessive blank lines.
    text = _MULTI_BLANK_LINE_RE.sub("\n\n", text)

    return text.strip()


# ---------------------------------------------------------------------------
# Repeated Punctuation
# ---------------------------------------------------------------------------

def normalize_repeated_punctuation(text: str) -> str:
    """
    Reduce noisy repeated punctuation commonly produced by
    OCR, PDF extraction, or badly formatted resumes.

    Examples:
        "Experience:::::: Python" -> "Experience: Python"
        "Skills!!!!"              -> "Skills!"
    """
    text = _ensure_text(text)

    return _REPEATED_PUNCTUATION_RE.sub(r"\1", text)


# ---------------------------------------------------------------------------
# Heading Normalization
# ---------------------------------------------------------------------------

def normalize_heading_casing(line: str) -> str:
    """
    Normalize likely section headings.

    Examples:
        SKILLS -> Skills
        WORK EXPERIENCE -> Work Experience
        education -> Education
    """

    line = _ensure_text(line)

    known_headings = {
        "skills",
        "work experience",
        "experience",
        "education",
        "certifications",
        "certification",
        "projects",
        "summary",
        "objective",
        "profile",
        "achievements",
        "languages",
        "contact",
        "contact information",
        "personal details",
    }

    stripped = line.strip()

    if not stripped:
        return line

    if len(stripped) > 40:
        return line

    # Structural marker inserted by the extractor.
    if stripped == "[TABLE]":
        return line

    lower = stripped.lower().rstrip(":")

    is_all_caps = (
        stripped.isupper()
        and len(stripped.split()) <= 4
    )

    is_known = lower in known_headings

    if is_all_caps or is_known:
        return stripped.rstrip(":").title()

    return line


def normalize_headings(text: str) -> str:
    """
    Normalize section heading casing throughout the document.
    """
    text = _ensure_text(text)

    return "\n".join(
        normalize_heading_casing(line)
        for line in text.split("\n")
    )


# ---------------------------------------------------------------------------
# Full Cleaning Pipeline
# ---------------------------------------------------------------------------

def clean_text(raw_text: str) -> str:
    """
    Full cleaning pass.

    Pipeline:
        1. Input validation
        2. Remove control/icon noise
        3. Normalize unicode
        4. Normalize repeated punctuation
        5. Normalize whitespace
    """

    text = _ensure_text(raw_text)

    if not text:
        return ""

    text = remove_control_and_icon_noise(text)
    text = normalize_unicode(text)
    text = normalize_repeated_punctuation(text)
    text = normalize_whitespace(text)

    return text


# ---------------------------------------------------------------------------
# Full Normalization Pipeline
# ---------------------------------------------------------------------------

def normalize_text(cleaned_text: str) -> str:
    """
    Full normalization pass on already-cleaned text.

    Pipeline:
        1. Normalize bullets
        2. Normalize headings
        3. Normalize whitespace
    """

    text = _ensure_text(cleaned_text)

    if not text:
        return ""

    text = normalize_bullets(text)
    text = normalize_headings(text)
    text = normalize_whitespace(text)

    return text


# ---------------------------------------------------------------------------
# Convenience Function
# ---------------------------------------------------------------------------

def clean_and_normalize_text(raw_text: str) -> str:
    """
    Run the complete cleaning + normalization pipeline.

    This is useful when the caller wants one function instead of
    calling clean_text() followed by normalize_text().
    """

    text = clean_text(raw_text)

    if not text:
        return ""

    return normalize_text(text)
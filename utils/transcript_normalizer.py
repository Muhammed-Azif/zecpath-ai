"""
Day 24 - Transcript Normalization Module

Cleans raw speech-to-text output before AI processing.
Handles filler words, punctuation, capitalization,
interrupted speech, partial answers and silence.
"""

import re
from typing import Optional


class TranscriptNormalizer:
    """
    Normalizes raw speech-to-text transcripts.
    """

    FILLER_WORDS = {
        "um",
        "uh",
        "erm",
        "er",
        "hmm",
        "hmmm",
        "like",
        "you know",
        "actually",
        "basically",
    }

    @staticmethod
    def remove_filler_words(text: str) -> str:
        """
        Remove common speech filler words and
        clean punctuation left behind by their removal.
        """

        if not text:
            return ""

        for filler in TranscriptNormalizer.FILLER_WORDS:
            pattern = r"\b" + re.escape(filler) + r"\b"
            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE
            )

        # Remove punctuation left at the beginning
        # after removing filler words.
        text = re.sub(r"^\s*[,;:]+\s*", "", text)

        # Remove spaces before punctuation.
        text = re.sub(r"\s+([,.!?])", r"\1", text)

        # Normalize repeated commas.
        text = re.sub(r",{2,}", ",", text)

        return text.strip()
   


    @staticmethod
    def normalize_case(text: str) -> str:
        """
        Normalize text capitalization.
        """

        if not text:
            return ""

        text = text.strip()

        if not text:
            return ""

        return text[0].upper() + text[1:]

    @staticmethod
    def normalize_spaces(text: str) -> str:
        """
        Remove unnecessary whitespace.
        """

        if not text:
            return ""

        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def normalize_punctuation(text: str) -> str:
        """
        Normalize basic punctuation.
        """

        if not text:
            return ""

        text = text.strip()

        # Remove spaces before punctuation
        text = re.sub(r"\s+([,.!?])", r"\1", text)

        # Collapse repeated punctuation
        text = re.sub(r"[.]{2,}", ".", text)
        text = re.sub(r"[!]{2,}", "!", text)
        text = re.sub(r"[?]{2,}", "?", text)

        # Add a period when no terminal punctuation exists
        if text and text[-1] not in ".!?":
            text += "."

        return text

    @staticmethod
    def handle_interrupted_speech(text: str) -> str:
        """
        Clean common interrupted speech patterns.

        Example:
            "I worked on Python but- actually I worked on Java."

        becomes:

            "I worked on Python but actually I worked on Java."
        """

        if not text:
            return ""

        # Remove interruption hyphens
        text = re.sub(r"\s*-\s*", " ", text)

        # Remove unfinished repeated words
        text = re.sub(
            r"\b(\w+)\s+\1\b",
            r"\1",
            text,
            flags=re.IGNORECASE,
        )

        return text

    @staticmethod
    def handle_partial_answer(text: str) -> str:
        """
        Preserve meaningful partial answers.

        Partial answers must not be replaced with invented content.
        """

        if not text:
            return ""

        text = text.strip()

        # Mark obvious incomplete speech without changing meaning.
        if text.endswith("-"):
            text = text[:-1].strip()

        return text

    @staticmethod
    def detect_silence(text: Optional[str]) -> bool:
        """
        Detect empty or silence-only transcript output.

        Returns True when no meaningful speech is present.
        """

        if not text:
            return True

        normalized = text.strip().lower()

        silence_patterns = {
            "",
            "[silence]",
            "[silent]",
            "(silence)",
            "[noise]",
            "[inaudible]",
            "[unintelligible]",
        }

        return normalized in silence_patterns

    @classmethod
    def normalize(cls, text: Optional[str]) -> str:
        """
        Apply the complete transcript normalization pipeline.
        """

        if cls.detect_silence(text):
            return ""

        text = cls.remove_filler_words(text)
        text = cls.handle_interrupted_speech(text)
        text = cls.handle_partial_answer(text)
        text = cls.normalize_spaces(text)
        text = cls.normalize_punctuation(text)
        text = cls.normalize_case(text)

        return text

    @classmethod
    def normalize_question(cls, text: Optional[str]) -> str:
        """
        Normalize screening question text.
        """

        text = cls.normalize(text)

        if text and not text.endswith("?"):
            text = text.rstrip(".") + "?"

        return text

    @classmethod
    def normalize_response(cls, text: Optional[str]) -> str:
        """
        Normalize candidate response text.
        """

        return cls.normalize(text)
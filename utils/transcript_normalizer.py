"""
Day 23 - Transcript Normalization

Provides basic normalization rules for AI processing
of voice screening transcripts.
"""

import re


class TranscriptNormalizer:
    """
    Normalizes raw speech-to-text output before
    sending it to downstream AI components.
    """

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize transcript text.
        """

        if not text:
            return ""

        # Remove leading/trailing whitespace
        text = text.strip()

        # Normalize multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Normalize common speech-to-text artifacts
        replacements = {
            " uh ": " ",
            " um ": " ",
            " er ": " ",
            " hmm ": " ",
        }

        padded_text = f" {text.lower()} "

        for old, new in replacements.items():
            padded_text = padded_text.replace(old, new)

        text = padded_text.strip()

        # Restore readable capitalization
        if text:
            text = text[0].upper() + text[1:]

        return text

    @staticmethod
    def normalize_question(text: str) -> str:
        """
        Normalize screening question text.
        """

        text = TranscriptNormalizer.normalize(text)

        if text and not text.endswith("?"):
            text += "?"

        return text

    @staticmethod
    def normalize_response(text: str) -> str:
        """
        Normalize candidate response text.
        """

        return TranscriptNormalizer.normalize(text)
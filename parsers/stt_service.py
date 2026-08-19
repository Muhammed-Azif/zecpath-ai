"""
Day 24 - Speech-to-Text Service Interface

Provides a provider-independent interface for converting
audio into raw transcript segments.

The default implementation is intentionally provider-neutral
so the rest of Zecpath AI does not depend on one STT vendor.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SpeechToTextService(ABC):
    """
    Base interface for speech-to-text providers.
    """

    @abstractmethod
    def transcribe(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Convert audio into transcript segments.
        """

        raise NotImplementedError


class MockSpeechToTextService(SpeechToTextService):
    """
    Test STT provider.

    Used for development and automated testing without
    requiring an external speech API.
    """

    def __init__(self, segments=None):
        self.segments = segments or []

    def transcribe(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Return predefined transcript segments.
        """

        return self.segments
"""
Day 24 - Clean Transcript Processor

Converts raw speech-to-text segments into clean,
AI-processable transcript data.
"""

from typing import Any, Dict, List

from utils.transcript_normalizer import TranscriptNormalizer


class CleanTranscriptProcessor:
    """
    Processes raw STT output into normalized transcript data.
    """

    def __init__(self):
        self.normalizer = TranscriptNormalizer()

    def process_segment(self, segment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean a single STT segment.
        """

        raw_text = segment.get("text", "")

        clean_text = self.normalizer.normalize(raw_text)

        processed_segment = dict(segment)

        processed_segment["raw_text"] = raw_text
        processed_segment["text"] = clean_text
        processed_segment["is_silence"] = not bool(clean_text)

        return processed_segment

    def process_segments(
        self,
        segments: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple STT segments.
        """

        processed = []

        for segment in segments:
            result = self.process_segment(segment)

            # Keep silence information but don't send empty
            # speech to downstream AI processing.
            if not result["is_silence"]:
                processed.append(result)

        return processed

    def process_transcript(
        self,
        transcript: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a complete transcript.
        """

        result = dict(transcript)

        raw_segments = transcript.get("segments", [])

        clean_segments = self.process_segments(raw_segments)

        result["segments"] = clean_segments

        # Rebuild clean interaction responses
        interactions = []

        for interaction in transcript.get("interactions", []):
            interaction_copy = dict(interaction)

            response = interaction_copy.get(
                "response_text",
                ""
            )

            interaction_copy["raw_response_text"] = response
            interaction_copy["response_text"] = (
                self.normalizer.normalize_response(response)
            )

            interactions.append(interaction_copy)

        result["interactions"] = interactions

        return result
"""
Day 24 - Transcript Processing Tests
"""

from processors.clean_transcript_processor import (
    CleanTranscriptProcessor,
)

from utils.transcript_normalizer import (
    TranscriptNormalizer,
)


def test_filler_words_removed():
    text = "Um, I have, uh, experience with Python."

    result = TranscriptNormalizer.normalize(text)

    assert "Um" not in result
    assert "uh" not in result.lower()
    assert "experience with Python" in result


def test_case_normalization():
    text = "i have experience with python"

    result = TranscriptNormalizer.normalize(text)

    assert result == "I have experience with python."


def test_punctuation_normalization():
    text = "I worked with Python   "

    result = TranscriptNormalizer.normalize(text)

    assert result == "I worked with Python."


def test_interrupted_speech():
    text = "I worked with Python - actually I worked with Java"

    result = TranscriptNormalizer.normalize(text)

    assert "-" not in result
    assert "Python" in result
    assert "Java" in result


def test_partial_answer():
    text = "I have experience with machine learning-"

    result = TranscriptNormalizer.normalize(text)

    assert result
    assert "machine learning" in result


def test_silence_detection():
    assert TranscriptNormalizer.detect_silence("[silence]")
    assert TranscriptNormalizer.detect_silence("")
    assert TranscriptNormalizer.detect_silence(None)


def test_normalized_silence_is_empty():
    result = TranscriptNormalizer.normalize("[silence]")

    assert result == ""


def test_clean_transcript_processor():

    transcript = {
        "transcript_id": "transcript_test",
        "candidate_id": "cand_001",
        "job_id": "job_001",
        "segments": [
            {
                "speaker": "candidate",
                "text": "Um, I have experience with Python",
                "timestamp": 10.0,
                "confidence": 0.95,
            },
            {
                "speaker": "candidate",
                "text": "[silence]",
                "timestamp": 20.0,
                "confidence": 0.50,
            },
        ],
        "interactions": [],
    }

    processor = CleanTranscriptProcessor()

    result = processor.process_transcript(transcript)

    assert len(result["segments"]) == 1

    assert (
        result["segments"][0]["text"]
        == "I have experience with Python."
    )

    assert result["segments"][0]["raw_text"] == (
        "Um, I have experience with Python"
    )
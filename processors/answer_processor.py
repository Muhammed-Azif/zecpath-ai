"""
Day 25 - Answer Processor

Connects cleaned transcript answers from Day 24
to the Answer Understanding Engine.
"""

from answer_engine.answer_understanding import AnswerUnderstandingEngine


class AnswerProcessor:

    def __init__(self):
        self.engine = AnswerUnderstandingEngine()

    def process_answer(
        self,
        answer: str,
        question: str = "",
        question_id: str = ""
    ) -> dict:

        return self.engine.understand(
            answer=answer,
            question=question,
            question_id=question_id
        )

    def process_transcript(self, transcript: dict) -> list:
        """
        Process all answer segments from a transcript.

        Expected transcript format:

        {
            "transcript_id": "...",
            "segments": [
                {
                    "question_id": "...",
                    "question": "...",
                    "text": "..."
                }
            ]
        }
        """

        results = []

        segments = transcript.get("segments", [])

        for segment in segments:

            answer = segment.get("text", "")

            result = self.process_answer(
                answer=answer,
                question=segment.get("question", ""),
                question_id=segment.get("question_id", "")
            )

            results.append(result)

        return results
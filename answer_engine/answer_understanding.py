"""
Day 25 - Answer Understanding Engine

Combines intent classification, information extraction,
quality detection and semantic structuring.
"""

from answer_engine.intent_classifier import IntentClassifier
from answer_engine.answer_extractor import AnswerExtractor
from answer_engine.answer_quality import AnswerQualityDetector


class AnswerUnderstandingEngine:

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.extractor = AnswerExtractor()
        self.quality_detector = AnswerQualityDetector()

    def understand(
        self,
        answer: str,
        question: str = "",
        question_id: str = ""
    ) -> dict:

        intent_result = self.intent_classifier.classify(answer)

        intent = intent_result["intent"]

        quality_result = self.quality_detector.check(
            answer,
            intent
        )

        entities = self.extractor.extract(
            answer,
            intent
        )

        return {
            "question_id": question_id,
            "question": question,
            "answer": answer.strip() if answer else "",
            "intent": intent,
            "confidence": intent_result["confidence"],
            "entities": entities,
            "quality": quality_result["quality"],
            "quality_reason": quality_result["reason"],
            "off_topic": intent == "off_topic",
            "matched_keywords": intent_result["matched_keywords"],
        }
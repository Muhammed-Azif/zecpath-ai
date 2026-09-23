from typing import Dict, Any


class FollowUpTrigger:
    """
    Determines whether a screening answer requires
    a follow-up question.
    """

    def evaluate(self, answer: Dict[str, Any]) -> Dict[str, Any]:
        intent = answer.get("intent", "unknown")
        quality = answer.get("quality", "unknown")
        entities = answer.get("entities", {})

        if quality == "missing":
            return self._trigger(
                "missing_answer",
                "Could you please provide an answer to the question?",
            )

        if quality in {"vague", "unclear"}:
            return self._trigger(
                "clarification",
                "Could you provide a little more detail?",
            )

        if answer.get("off_topic", False):
            return self._trigger(
                "off_topic",
                "Let's focus on the screening question. Could you answer that directly?",
            )

        if intent == "experience" and not entities.get("experience"):
            return self._trigger(
                "experience_clarification",
                "Could you tell me approximately how many years of experience you have?",
            )

        if intent == "salary" and not entities.get("salary"):
            return self._trigger(
                "salary_clarification",
                "Could you provide your expected annual salary?",
            )

        if intent == "availability" and not entities.get("availability"):
            return self._trigger(
                "availability_clarification",
                "Could you clarify when you would be available to join?",
            )

        if intent == "skill" and entities.get("skills"):
            return self._trigger(
                "skill_follow_up",
                "Could you describe your practical experience with that skill?",
            )

        return {
            "triggered": False,
            "trigger": None,
            "question": None,
        }

    @staticmethod
    def _trigger(trigger_name: str, question: str) -> Dict[str, Any]:
        return {
            "triggered": True,
            "trigger": trigger_name,
            "question": question,
        }
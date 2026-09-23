from typing import Dict


class ConversationErrorHandler:
    """
    Provides polite recovery messages for conversation errors.
    """

    MESSAGES = {
        "silence": (
            "I didn't hear a response. "
            "Could you please answer the question?"
        ),
        "confusion": (
            "No problem. Let me ask that in a simpler way."
        ),
        "repeated": (
            "Thank you. I'd like to ask that question "
            "in a slightly different way."
        ),
        "off_topic": (
            "Thank you. Let's return to the screening question."
        ),
        "processing_error": (
            "I'm having a little trouble processing that response. "
            "Could you please try again?"
        ),
        "max_retries": (
            "It looks like we're having difficulty with this question. "
            "We'll move on to the next part of the screening."
        ),
    }

    def get_message(self, error_type: str) -> Dict[str, str]:
        message = self.MESSAGES.get(error_type)

        if message is None:
            message = (
                "I'm sorry, I couldn't process that response. "
                "Let's try again."
            )

        return {
            "error_type": error_type,
            "message": message,
        }
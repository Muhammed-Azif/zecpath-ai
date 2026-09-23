from conversation.conversation_state import (
    ConversationState,
    ConversationStateMachine,
)


class ConversationFlow:
    """
    Controls the flow of an AI screening conversation.
    """

    def __init__(self, max_retries=2):
        self.state_machine = ConversationStateMachine()
        self.max_retries = max_retries
        self.retry_count = 0
        self.current_question = None

    def start_question(self, question):
        """Start asking a screening question."""
        self.current_question = question
        self.retry_count = 0

        self.state_machine.transition_to(
            ConversationState.ASKING
        )

        return {
            "state": self.state_machine.get_state().value,
            "question": question,
        }

    def receive_answer(self, answer_status):
        """
        Process the result of an answer.

        Supported statuses:
        valid
        silence
        confused
        repeated
        off_topic
        """

        self.state_machine.transition_to(
            ConversationState.PROCESSING
        )

        handlers = {
            "valid": self._handle_valid_answer,
            "silence": self._handle_silence,
            "confused": self._handle_confused,
            "repeated": self._handle_repeated,
            "off_topic": self._handle_off_topic,
        }

        handler = handlers.get(answer_status)

        if handler is None:
            raise ValueError(
                f"Unknown answer status: {answer_status}"
            )

        return handler()

    def _handle_valid_answer(self):
        self.retry_count = 0

        self.state_machine.transition_to(
            ConversationState.VALID_ANSWER
        )

        return {
            "state": "valid_answer",
            "action": "continue",
            "message": "Thank you. Let's continue.",
        }

    def _handle_silence(self):
        self.retry_count += 1

        self.state_machine.transition_to(
            ConversationState.SILENCE
        )

        if self.retry_count > self.max_retries:
            return self._handle_failure()

        self.state_machine.transition_to(
            ConversationState.RETRY
        )

        return {
            "state": "retry",
            "reason": "silence",
            "retry_count": self.retry_count,
            "action": "repeat_question",
            "message": "I didn't hear a response. Could you please answer the question?",
        }

    def _handle_confused(self):
        self.retry_count += 1

        self.state_machine.transition_to(
            ConversationState.CONFUSED
        )

        if self.retry_count > self.max_retries:
            return self._handle_failure()

        self.state_machine.transition_to(
            ConversationState.FOLLOW_UP
        )

        return {
            "state": "follow_up",
            "reason": "confusion",
            "retry_count": self.retry_count,
            "action": "clarify_question",
            "message": "Let me rephrase that. Could you explain it in a simpler way?",
        }

    def _handle_repeated(self):
        self.retry_count += 1

        self.state_machine.transition_to(
            ConversationState.REPEATED
        )

        if self.retry_count > self.max_retries:
            return self._handle_failure()

        self.state_machine.transition_to(
            ConversationState.RETRY
        )

        return {
            "state": "retry",
            "reason": "repeated_answer",
            "retry_count": self.retry_count,
            "action": "rephrase_question",
            "message": "Thank you. I'd like to ask that in a slightly different way.",
        }

    def _handle_off_topic(self):
        self.retry_count += 1

        self.state_machine.transition_to(
            ConversationState.OFF_TOPIC
        )

        if self.retry_count > self.max_retries:
            return self._handle_failure()

        self.state_machine.transition_to(
            ConversationState.FOLLOW_UP
        )

        return {
            "state": "follow_up",
            "reason": "off_topic",
            "retry_count": self.retry_count,
            "action": "redirect",
            "message": "Thank you. Let's return to the screening question.",
        }

    def _handle_failure(self):
        self.state_machine.transition_to(
            ConversationState.FAILED
        )

        return {
            "state": "failed",
            "action": "graceful_exit",
            "message": (
                "I'm sorry, but we couldn't complete this question. "
                "We'll move forward with the screening process."
            ),
        }

    def complete(self):
        """Complete the conversation."""
        self.state_machine.transition_to(
            ConversationState.COMPLETED
        )

        return {
            "state": "completed",
            "message": "Thank you for completing the screening.",
        }
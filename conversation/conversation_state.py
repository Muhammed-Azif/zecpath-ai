from enum import Enum


class ConversationState(Enum):
    START = "start"
    ASKING = "asking"
    LISTENING = "listening"
    PROCESSING = "processing"
    VALID_ANSWER = "valid_answer"
    SILENCE = "silence"
    CONFUSED = "confused"
    REPEATED = "repeated"
    OFF_TOPIC = "off_topic"
    FOLLOW_UP = "follow_up"
    RETRY = "retry"
    COMPLETED = "completed"
    FAILED = "failed"


class ConversationStateMachine:
    """
    Controls the current state of an AI screening conversation.
    """

    def __init__(self):
        self.current_state = ConversationState.START
        self.previous_state = None

    def transition_to(self, new_state: ConversationState):
        """
        Move the conversation to a new state.
        """
        if not isinstance(new_state, ConversationState):
            raise ValueError("Invalid conversation state")

        self.previous_state = self.current_state
        self.current_state = new_state

        return self.current_state

    def get_state(self):
        """
        Return the current conversation state.
        """
        return self.current_state

    def get_previous_state(self):
        """
        Return the previous conversation state.
        """
        return self.previous_state

    def reset(self):
        """
        Reset the conversation to the START state.
        """
        self.previous_state = None
        self.current_state = ConversationState.START

    def is_finished(self):
        """
        Check whether the conversation has reached a terminal state.
        """
        return self.current_state in {
            ConversationState.COMPLETED,
            ConversationState.FAILED,
        }
from conversation.conversation_state import (
    ConversationState,
    ConversationStateMachine,
)


def main():
    machine = ConversationStateMachine()

    print("Initial state:", machine.get_state().value)

    machine.transition_to(ConversationState.ASKING)
    print("Current state:", machine.get_state().value)

    machine.transition_to(ConversationState.LISTENING)
    print("Current state:", machine.get_state().value)

    machine.transition_to(ConversationState.PROCESSING)
    print("Current state:", machine.get_state().value)

    machine.transition_to(ConversationState.VALID_ANSWER)
    print("Current state:", machine.get_state().value)

    machine.transition_to(ConversationState.FOLLOW_UP)
    print("Current state:", machine.get_state().value)

    machine.transition_to(ConversationState.COMPLETED)
    print("Current state:", machine.get_state().value)

    print("Previous state:", machine.get_previous_state().value)
    print("Conversation finished:", machine.is_finished())


if __name__ == "__main__":
    main()
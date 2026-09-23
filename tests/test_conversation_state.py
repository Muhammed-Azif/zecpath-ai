from conversation.conversation_state import (
    ConversationState,
    ConversationStateMachine,
)


def test_initial_state():
    machine = ConversationStateMachine()

    assert machine.get_state() == ConversationState.START


def test_state_transition():
    machine = ConversationStateMachine()

    machine.transition_to(ConversationState.ASKING)

    assert machine.get_state() == ConversationState.ASKING


def test_previous_state():
    machine = ConversationStateMachine()

    machine.transition_to(ConversationState.ASKING)
    machine.transition_to(ConversationState.LISTENING)

    assert machine.get_previous_state() == ConversationState.ASKING


def test_reset():
    machine = ConversationStateMachine()

    machine.transition_to(ConversationState.COMPLETED)
    machine.reset()

    assert machine.get_state() == ConversationState.START
    assert machine.get_previous_state() is None


def test_completed_state():
    machine = ConversationStateMachine()

    machine.transition_to(ConversationState.COMPLETED)

    assert machine.is_finished() is True


def test_failed_state():
    machine = ConversationStateMachine()

    machine.transition_to(ConversationState.FAILED)

    assert machine.is_finished() is True
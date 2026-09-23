from conversation.conversation_flow import ConversationFlow


def test_start_question():
    flow = ConversationFlow()

    result = flow.start_question(
        "Tell me about your experience."
    )

    assert result["state"] == "asking"
    assert result["question"] == "Tell me about your experience."


def test_valid_answer():
    flow = ConversationFlow()

    flow.start_question("Tell me about Python.")
    result = flow.receive_answer("valid")

    assert result["state"] == "valid_answer"
    assert result["action"] == "continue"


def test_silence_triggers_retry():
    flow = ConversationFlow()

    flow.start_question("What is your notice period?")
    result = flow.receive_answer("silence")

    assert result["state"] == "retry"
    assert result["reason"] == "silence"


def test_confusion_triggers_clarification():
    flow = ConversationFlow()

    flow.start_question("Explain your technical experience.")
    result = flow.receive_answer("confused")

    assert result["state"] == "follow_up"
    assert result["reason"] == "confusion"
    assert result["action"] == "clarify_question"


def test_repeated_answer_triggers_rephrase():
    flow = ConversationFlow()

    flow.start_question("What is your salary expectation?")
    result = flow.receive_answer("repeated")

    assert result["state"] == "retry"
    assert result["reason"] == "repeated_answer"


def test_off_topic_triggers_redirect():
    flow = ConversationFlow()

    flow.start_question("How many years of experience do you have?")
    result = flow.receive_answer("off_topic")

    assert result["state"] == "follow_up"
    assert result["reason"] == "off_topic"


def test_max_retries_causes_failure():
    flow = ConversationFlow(max_retries=2)

    flow.start_question("What is your availability?")

    flow.receive_answer("silence")
    flow.receive_answer("silence")
    result = flow.receive_answer("silence")

    assert result["state"] == "failed"
    assert result["action"] == "graceful_exit"


def test_complete_conversation():
    flow = ConversationFlow()

    flow.start_question("Tell me about yourself.")
    result = flow.complete()

    assert result["state"] == "completed"
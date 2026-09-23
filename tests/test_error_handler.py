from conversation.error_handler import ConversationErrorHandler


def test_silence_message():
    handler = ConversationErrorHandler()

    result = handler.get_message("silence")

    assert result["error_type"] == "silence"
    assert "response" in result["message"]


def test_confusion_message():
    handler = ConversationErrorHandler()

    result = handler.get_message("confusion")

    assert "simpler" in result["message"]


def test_repeated_message():
    handler = ConversationErrorHandler()

    result = handler.get_message("repeated")

    assert "different way" in result["message"]


def test_off_topic_message():
    handler = ConversationErrorHandler()

    result = handler.get_message("off_topic")

    assert "screening question" in result["message"]


def test_processing_error():
    handler = ConversationErrorHandler()

    result = handler.get_message("processing_error")

    assert "processing" in result["message"]


def test_max_retries():
    handler = ConversationErrorHandler()

    result = handler.get_message("max_retries")

    assert "next part" in result["message"]


def test_unknown_error():
    handler = ConversationErrorHandler()

    result = handler.get_message("unknown")

    assert result["message"]
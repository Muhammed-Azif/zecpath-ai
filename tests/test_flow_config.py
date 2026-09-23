from conversation.flow_config import ConversationFlowConfig


def test_config_loads():
    config = ConversationFlowConfig()

    assert config.get("version") == "1.0"


def test_max_retries():
    config = ConversationFlowConfig()

    assert config.get(
        "conversation",
        "max_retries"
    ) == 2


def test_silence_configuration():
    config = ConversationFlowConfig()

    assert config.get(
        "silence",
        "enabled"
    ) is True

    assert config.get(
        "silence",
        "action"
    ) == "retry"


def test_confusion_configuration():
    config = ConversationFlowConfig()

    assert config.get(
        "confusion",
        "action"
    ) == "clarify"


def test_failure_configuration():
    config = ConversationFlowConfig()

    assert config.get(
        "failure",
        "action"
    ) == "graceful_exit"


def test_missing_configuration_returns_default():
    config = ConversationFlowConfig()

    result = config.get(
        "something",
        "does_not_exist",
        default="default_value"
    )

    assert result == "default_value"
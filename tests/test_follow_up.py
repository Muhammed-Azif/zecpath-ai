from conversation.follow_up import FollowUpTrigger


def test_missing_answer():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "unknown",
        "quality": "missing",
        "entities": {},
        "off_topic": False,
    })

    assert result["triggered"] is True
    assert result["trigger"] == "missing_answer"


def test_vague_answer():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "experience",
        "quality": "vague",
        "entities": {},
        "off_topic": False,
    })

    assert result["triggered"] is True
    assert result["trigger"] == "clarification"


def test_off_topic_answer():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "unknown",
        "quality": "valid",
        "entities": {},
        "off_topic": True,
    })

    assert result["triggered"] is True
    assert result["trigger"] == "off_topic"


def test_experience_follow_up():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "experience",
        "quality": "valid",
        "entities": {},
        "off_topic": False,
    })

    assert result["trigger"] is not None
    assert result["trigger"] == "experience_clarification"


def test_salary_follow_up():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "salary",
        "quality": "valid",
        "entities": {},
        "off_topic": False,
    })

    assert result["trigger"] == "salary_clarification"


def test_availability_follow_up():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "availability",
        "quality": "valid",
        "entities": {},
        "off_topic": False,
    })

    assert result["trigger"] == "availability_clarification"


def test_skill_follow_up():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "skill",
        "quality": "valid",
        "entities": {
            "skills": ["Python"]
        },
        "off_topic": False,
    })

    assert result["trigger"] == "skill_follow_up"


def test_no_follow_up_for_complete_answer():
    trigger = FollowUpTrigger()

    result = trigger.evaluate({
        "intent": "experience",
        "quality": "valid",
        "entities": {
            "experience": 3
        },
        "off_topic": False,
    })

    assert result["triggered"] is False
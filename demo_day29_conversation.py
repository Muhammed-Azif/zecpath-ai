from conversation.conversation_flow import ConversationFlow
from conversation.follow_up import FollowUpTrigger
from conversation.error_handler import ConversationErrorHandler
from conversation.flow_config import ConversationFlowConfig


def main():
    print("=" * 70)
    print("ZECPATH AI - DAY 29 CONVERSATION FLOW DEMO")
    print("=" * 70)

    config = ConversationFlowConfig()

    print("\nConfiguration")
    print("-" * 70)
    print("Version:", config.get("version"))
    print(
        "Maximum retries:",
        config.get("conversation", "max_retries")
    )

    flow = ConversationFlow(
        max_retries=config.get(
            "conversation",
            "max_retries"
        )
    )

    follow_up = FollowUpTrigger()
    error_handler = ConversationErrorHandler()

    # ---------------------------------------------------------
    # Question 1
    # ---------------------------------------------------------

    print("\nQUESTION 1")
    print("-" * 70)

    result = flow.start_question(
        "Can you describe your experience with Python?"
    )

    print("State:", result["state"])
    print("Question:", result["question"])

    answer = {
        "intent": "skill",
        "quality": "valid",
        "entities": {
            "skills": ["Python"]
        },
        "off_topic": False
    }

    print("\nAnswer analysis:")
    print(answer)

    trigger = follow_up.evaluate(answer)

    print("\nFollow-up:")
    print(trigger)

    # ---------------------------------------------------------
    # Question 2 - Silence
    # ---------------------------------------------------------

    print("\nQUESTION 2")
    print("-" * 70)

    flow.start_question(
        "What is your current notice period?"
    )

    print("Answer status: silence")

    result = flow.receive_answer("silence")

    print(result)

    error = error_handler.get_message("silence")
    print("AI response:", error["message"])

    # ---------------------------------------------------------
    # Question 3 - Confusion
    # ---------------------------------------------------------

    print("\nQUESTION 3")
    print("-" * 70)

    flow.start_question(
        "What are your salary expectations?"
    )

    print("Answer status: confused")

    result = flow.receive_answer("confused")

    print(result)

    error = error_handler.get_message("confusion")
    print("AI response:", error["message"])

    # ---------------------------------------------------------
    # Question 4 - Off Topic
    # ---------------------------------------------------------

    print("\nQUESTION 4")
    print("-" * 70)

    flow.start_question(
        "How many years of professional experience do you have?"
    )

    print("Answer status: off_topic")

    result = flow.receive_answer("off_topic")

    print(result)

    error = error_handler.get_message("off_topic")
    print("AI response:", error["message"])

    # ---------------------------------------------------------
    # Complete
    # ---------------------------------------------------------

    print("\nCOMPLETING SCREENING")
    print("-" * 70)

    result = flow.complete()

    print(result)

    print("\n" + "=" * 70)
    print("DAY 29 CONVERSATION FLOW DEMO COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
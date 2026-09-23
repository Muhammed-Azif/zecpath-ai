from conversation.conversation_flow import ConversationFlow


def main():
    flow = ConversationFlow(max_retries=2)

    print("=" * 60)
    print("ZECPATH AI - CONVERSATION FLOW DEMO")
    print("=" * 60)

    result = flow.start_question(
        "Can you describe your experience with Python?"
    )

    print("\nQUESTION")
    print(result)

    print("\nANSWER: VALID")
    print(flow.receive_answer("valid"))

    print("\nQUESTION")
    flow.start_question(
        "What is your current notice period?"
    )

    print("\nANSWER: SILENCE")
    print(flow.receive_answer("silence"))

    print("\nANSWER: CONFUSED")
    print(flow.receive_answer("confused"))

    print("\nANSWER: VALID")
    print(flow.receive_answer("valid"))

    print("\nCOMPLETING CONVERSATION")
    print(flow.complete())


if __name__ == "__main__":
    main()
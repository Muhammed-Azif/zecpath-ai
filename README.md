## Day 29 – AI Conversation Flow Design

### Objective

Designed the dynamic conversation flow used by Zecpath AI during AI-based screening calls.

### Implemented Features

* AI conversation state machine
* Dynamic question flow
* Silence detection and retry handling
* Confusion handling and question clarification
* Repeated-answer detection and question rephrasing
* Off-topic answer redirection
* Follow-up question triggers
* Missing and vague answer handling
* Configurable retry limits
* Graceful failure and retry logic
* Conversation completion handling
* Automated test coverage

### Conversation States

The conversation state machine supports:

* START
* ASKING
* LISTENING
* PROCESSING
* VALID_ANSWER
* SILENCE
* CONFUSED
* REPEATED
* OFF_TOPIC
* FOLLOW_UP
* RETRY
* COMPLETED
* FAILED

### Conversation Flow

```text
START
  ↓
ASK QUESTION
  ↓
LISTEN
  ↓
PROCESS ANSWER
  │
  ├── Valid Answer ──────→ Continue
  │
  ├── Silence ───────────→ Retry / Fallback
  │
  ├── Confusion ─────────→ Clarify
  │
  ├── Repeated Answer ───→ Rephrase
  │
  └── Off Topic ─────────→ Redirect
                              ↓
                         Retry Limit
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
                  Retry              Graceful
                                     Failure
```

### Follow-Up Triggers

The follow-up engine identifies situations requiring additional questions, including:

* Missing answers
* Vague answers
* Off-topic answers
* Missing experience information
* Missing salary information
* Missing availability information
* Skill-related follow-up questions

### Error Handling

The conversation error handler provides polite responses for:

* Silence
* Confusion
* Repeated answers
* Off-topic responses
* Processing errors
* Maximum retry attempts

### Configuration

Conversation behavior is configurable through:

`data/conversation_flow_config.json`

Configurable parameters include:

* Maximum retries
* Silence handling
* Confusion handling
* Repeated-answer handling
* Off-topic handling
* Fallback behavior
* Graceful failure behavior

### Testing

Day 29 functionality is covered by automated tests for:

* Conversation states
* State transitions
* Conversation flow
* Follow-up triggers
* Error handling
* Configuration loading

All project tests passed successfully after the Day 29 implementation.

### Day 29 Deliverables

1. AI Call Flow Logic
2. Conversation State Machine
3. Error-Handling Flow Design

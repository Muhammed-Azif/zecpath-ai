# Zecpath AI ATS Architecture

## 1. System Architecture

```text
                    ┌──────────────────────┐
                    │      Client/User     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      API Layer       │
                    │  Upload / Job /      │
                    │      Results         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Async Job Handler   │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │       Resume Processing         │
              └────────────────┬────────────────┘
                               │
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
     │ Text         │  │ Resume       │  │ File         │
     │ Extraction   │  │ Parsing      │  │ Validation   │
     └──────┬───────┘  └──────┬───────┘  └──────────────┘
            │                 │
            └────────┬────────┘
                     ▼
            ┌──────────────────┐
            │ Skill Extraction │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Skill Normalizer │
            └────────┬─────────┘
                     │
                     ▼
       ┌──────────────────────────────┐
       │       ATS Evaluation         │
       │                              │
       │ Skills                       │
       │ Experience                   │
       │ Education                    │
       │ Semantic Matching            │
       └──────────────┬───────────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    ATS Scorer   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │  Final Result   │
             └─────────────────┘

2.RESUME PROCESSING FLOW

Resume
  │
  ▼
Upload
  │
  ▼
Validation
  │
  ▼
Create Processing Job
  │
  ▼
Extract Text
  │
  ▼
Parse Resume
  │
  ▼
Extract Skills
  │
  ▼
Normalize Skills
  │
  ▼
Calculate Component Scores
  │
  ├── Skills Score
  ├── Experience Score
  ├── Education Score
  └── Semantic Score
          │
          ▼
     Weighted ATS Score
          │
          ▼
     Store/Return Result

3.SCORING ARCHITECTURE

                 ┌─────────────────┐
                 │  Resume + Job   │
                 └────────┬────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
     ┌─────────┐    ┌────────────┐   ┌────────────┐
     │ Skills  │    │ Experience │   │ Education  │
     └────┬────┘    └─────┬──────┘   └─────┬──────┘
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │   Semantic   │
                  │   Matching   │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Role Weights │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  ATS Scorer  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Final Score  │
                  └──────────────┘

4.JOB STATE FLOW

              ┌─────────┐
              │ PENDING │
              └────┬────┘
                   │
                   ▼
            ┌────────────┐
            │ PROCESSING │
            └─────┬──────┘
                  │
          ┌───────┴────────┐
          ▼                ▼
   ┌────────────┐    ┌────────┐
   │ COMPLETED  │    │ FAILED │
   └────────────┘    └────────┘

5. Architecture Principles

The ATS follows these principles:

Separation of concerns
Modular components
Configurable scoring
Asynchronous processing
Centralized error handling
Structured logging
Testability
Extensibility


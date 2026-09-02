# Zecpath AI

## AI-Powered Resume Screening and Candidate Evaluation System

Zecpath AI is an AI-powered recruitment and candidate screening system designed to automate resume analysis, ATS scoring, candidate eligibility decisions, HR screening, speech-to-text processing, answer understanding, and screening response evaluation.

The project is being developed incrementally with a modular architecture.

---

# Features

## Resume Processing

- Resume upload and parsing
- Resume text extraction
- Structured resume data processing
- Skill extraction
- Skill normalization
- Skill confidence scoring
- Experience extraction
- Education extraction

## Job Description Processing

- Job description parsing
- Required skill extraction
- Role-based evaluation
- Candidate-job matching

## Semantic Matching

- Semantic similarity matching
- Resume and job description comparison
- Sentence Transformer integration
- AI-based candidate relevance evaluation

Model used:

```text
sentence-transformers/all-MiniLM-L6-v2

ATS Scoring Engine

The ATS engine evaluates candidates using multiple factors:

Skills score
Experience score
Education score
Semantic similarity score

Example scoring workflow:

Resume
   ↓
Resume Parsing
   ↓
Skill Extraction
   ↓
Experience Analysis
   ↓
Education Analysis
   ↓
Semantic Matching
   ↓
ATS Score

The ATS engine also provides explainable score breakdowns.

Eligibility Decision Engine

The eligibility engine automatically determines whether a candidate should proceed to AI screening.

Decision factors include:

Minimum ATS score
Mandatory skills
Experience requirements
Location constraints
Availability constraints
Role-specific rules

Candidate decisions:

Eligible
Review
Rejected
HR Screening Dataset

Zecpath AI includes an AI-ready HR screening question dataset.

Question categories include:

Introduction
Education
Experience
Skills
Location
Salary
Notice Period

The dataset is designed for automated candidate screening conversations.

Transcript Architecture

The transcript system provides a structured architecture for storing candidate screening conversations.

Example workflow:

Candidate Speech
       ↓
Speech-to-Text
       ↓
Transcript
       ↓
Structured Transcript Data

The transcript architecture supports:

Transcript IDs
Question IDs
Candidate responses
Structured conversation segments
Transcript validation
Speech-to-Text and Transcript Processing

The speech processing system handles candidate responses after speech recognition.

Features include:

Speech-to-text integration
Transcript cleaning
Filler word removal
Case normalization
Punctuation normalization
Interrupted speech handling
Partial answer handling
Silence detection
Speech accuracy testing

Processing pipeline:

Candidate Speech
       ↓
Speech-to-Text
       ↓
Raw Transcript
       ↓
Transcript Cleaning
       ↓
Normalized Candidate Response
Answer Intent and Understanding Engine

The Answer Understanding Engine enables Zecpath AI to understand what the candidate actually means.

It performs:

Intent classification
Skill extraction
Experience extraction
Availability extraction
Salary expectation extraction
Off-topic response detection
Missing answer detection
Vague answer detection
Structured semantic answer generation

Supported intents include:

Skills
Experience
Availability
Salary
Education
Location
Introduction
Notice Period
Off-topic
Unknown

Example structured answer:

{
    "question_id": "q_skills_001",
    "intent": "skills",
    "answer": "I have experience with Python, SQL and machine learning.",
    "entities": {
        "skills": [
            "python",
            "sql",
            "machine learning"
        ]
    },
    "quality": "complete",
    "confidence": 0.95,
    "off_topic": false
}

Answer understanding pipeline:

Cleaned Candidate Answer
          ↓
Intent Classification
          ↓
Information Extraction
          ↓
Quality Detection
          ↓
Structured Semantic Answer
Screening Scoring Engine

The Screening Scoring Engine objectively evaluates candidate screening responses.

Each candidate answer is evaluated using four parameters:

Clarity

Measures how clear and understandable the candidate response is.

Relevance

Measures whether the response is relevant to the screening context.

Completeness

Measures whether the candidate provided sufficient information.

Consistency

Measures whether the response is semantically consistent with the extracted information.

Scoring Weights
Clarity        25%
Relevance      30%
Completeness   25%
Consistency    20%
-------------------
Total         100%
Per-Question Scoring

Each candidate response receives an individual score.

Example:

Question
   ↓
Clarity Score
Relevance Score
Completeness Score
Consistency Score
   ↓
Weighted Question Score

Example score object:

{
    "question_id": "q_001",
    "intent": "skills",
    "scores": {
        "clarity": 95.0,
        "relevance": 100.0,
        "completeness": 100.0,
        "consistency": 100.0
    },
    "weighted_score": 98.75,
    "quality": "complete",
    "off_topic": false
}
Final Screening Score

All question scores are aggregated into a final screening score.

Candidate Responses
        ↓
Per-Question Scoring
        ↓
Score Aggregation
        ↓
Score Normalization
        ↓
Final Screening Score
        ↓
Candidate Classification

Score classifications:

85 - 100    Excellent
70 - 84     Good
50 - 69     Average
0 - 49      Needs Improvement

Example final screening result:

{
    "total_score": 380.5,
    "normalized_score": 76.1,
    "classification": "Good",
    "questions_scored": 5
}

The engine also provides explainable outputs describing why the candidate received each score.

Complete AI Screening Pipeline
Resume
   ↓
Resume Parsing
   ↓
Skill & Experience Extraction
   ↓
Semantic Matching
   ↓
ATS Scoring
   ↓
Eligibility Decision
   ↓
HR Screening Questions
   ↓
Candidate Speech Response
   ↓
Speech-to-Text
   ↓
Transcript Cleaning
   ↓
Answer Intent & Understanding
   ↓
Screening Response Scoring
   ↓
Final Screening Score
Project Structure
zecpath-ai/
│
├── ats_engine/
│   ├── ats_scorer.py
│   ├── score_explainer.py
│   └── weight_config.py
│
├── answer_engine/
│   ├── __init__.py
│   ├── intent_classifier.py
│   ├── answer_extractor.py
│   ├── answer_quality.py
│   └── answer_understanding.py
│
├── screening_engine/
│   ├── __init__.py
│   ├── scoring_parameters.py
│   ├── response_scorer.py
│   ├── score_normalizer.py
│   ├── screening_aggregator.py
│   ├── score_explainer.py
│   └── screening_engine.py
│
├── parsers/
│
├── processors/
│   └── answer_processor.py
│
├── semantic_matching/
│
├── utils/
│
├── data/
│
├── tests/
│   ├── test_transcript_processing.py
│   ├── test_answer_understanding.py
│   └── test_screening_scoring.py
│
├── demo_ats.py
├── demo_answer_understanding.py
├── demo_day25_pipeline.py
├── demo_screening_scoring.py
│
└── README.md
Installation

Clone the repository:

git clone <repository-url>

Move into the project directory:

cd zecpath-ai

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Running the Demos
ATS Demo
python demo_ats.py
Answer Understanding Demo
python demo_answer_understanding.py
Day 25 Pipeline Demo
python demo_day25_pipeline.py
Day 26 Screening Scoring Demo
python demo_screening_scoring.py
Running Tests

Run all tests:

pytest -v

Run Day 25 tests:

pytest tests/test_answer_understanding.py -v

Run Day 26 tests:

pytest tests/test_screening_scoring.py -v
Development Progress
Day	Feature	Status
Day 21	Eligibility Decision Engine	Completed
Day 22	HR Screening Question Dataset	Completed
Day 23	Transcript Data Architecture	Completed
Day 24	Speech-to-Text and Transcript Cleaning	Completed
Day 25	Answer Intent and Understanding Engine	Completed
Day 26	Screening Scoring Engine	Completed
Current System Architecture
                    ZECPATH AI
                        │
                        ▼
                Resume Processing
                        │
                        ▼
                 ATS Scoring Engine
                        │
                        ▼
             Eligibility Decision Engine
                        │
                        ▼
               HR Screening Questions
                        │
                        ▼
               Candidate Speech Input
                        │
                        ▼
                 Speech-to-Text
                        │
                        ▼
               Transcript Processing
                        │
                        ▼
          Answer Intent & Understanding
                        │
                        ▼
             Screening Scoring Engine
                        │
                        ▼
              Final Screening Score
Current Status

Zecpath AI has successfully completed development through Day 26.

The system can now:

Parse candidate resumes
Extract candidate skills and experience
Perform semantic job matching
Generate ATS scores
Make eligibility decisions
Process HR screening questions
Convert candidate speech into text
Clean and normalize transcripts
Understand candidate answer intent
Extract semantic information from answers
Detect vague, missing and off-topic answers
Score candidate responses
Generate per-question score breakdowns
Generate normalized final screening scores
Provide explainable screening results
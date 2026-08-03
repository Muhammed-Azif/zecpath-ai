# Day 15 – Fairness, Normalization & Bias Reduction

## Objective

Improve fairness, reduce bias, and standardize resume evaluation before final candidate selection.

This module ensures that every resume is evaluated using only job-related information while removing personal attributes that could introduce bias into the recruitment process.

---

## Features

### 1. Resume Normalization
- Standardizes resume text formatting
- Removes unnecessary whitespace
- Creates consistent input for downstream AI modules

### 2. Bias Detection & Masking
Automatically removes or masks sensitive personal information such as:
- Email address
- Phone number
- Gender
- Age
- Marital status

This ensures candidate evaluation is based only on qualifications and skills.

### 3. Score Normalization
Normalizes ATS scores to a valid range (0–100).

Example:

Input: 108.4

Output: 100

Input: -12

Output: 0

---

## Project Structure

```
screening_ai/
│
├── bias_detector.py
├── fairness_engine.py
├── resume_normalizer.py
├── score_normalizer.py
└── __init__.py

tests/
└── test_fairness.py
```

---

## Workflow

```
Resume
    │
    ▼
Resume Normalizer
    │
    ▼
Bias Detector
    │
    ▼
Personal Information Masking
    │
    ▼
ATS Score Normalizer
    │
    ▼
Fair Resume + Normalized Score
```

---

## Files

### resume_normalizer.py
Standardizes resume formatting before processing.

### bias_detector.py
Masks personal information using regular expressions.

### score_normalizer.py
Ensures ATS scores remain within the valid range.

### fairness_engine.py
Integrates all fairness components into one processing pipeline.

### test_fairness.py
Demonstrates the fairness pipeline using a sample resume.

---

## How to Run

Activate the virtual environment.

```
venv\Scripts\activate
```

Run the test:

```
python -m tests.test_fairness
```

---

## Sample Output

```
==================================================
ZECPATH FAIRNESS ENGINE
==================================================

[MASKED]
[MASKED]

[MASKED]

[MASKED]

Python Developer

Normalized Score : 88.70

Bias Removed : True
```

---

## Deliverables

✔ Fair scoring improvements

✔ Resume normalization logic

✔ Bias reduction module

✔ Automated fairness engine

✔ Test script

---

## Technologies Used

- Python 3
- Regular Expressions (re)
- Object-Oriented Programming
- Rule-based NLP
- Modular AI Pipeline

---

## Integration

This module works after:

- Day 5 – Resume Text Extraction
- Day 6 – Job Description Parser
- Day 7 – Resume Section Classification
- Day 8 – Education Parser
- Day 9 – Skill Extraction
- Day 10 – Experience Parser
- Day 12 – Semantic Matching
- Day 13 – ATS Scoring
- Day 14 – Candidate Ranking

Pipeline:

Resume
→ Parsing
→ Skill Extraction
→ Semantic Matching
→ ATS Scoring
→ Candidate Ranking
→ Fairness Engine
→ Final Candidate Selection

---

## Future Improvements

- AI-based bias detection using NLP models
- Location and nationality masking
- Fairness analytics dashboard
- Explainable AI (XAI) fairness reports
- Bias score visualization
- Recruiter fairness audit logs

---

## Status

**Day 15 Completed**

All required deliverables have been implemented:
- Resume normalization
- Bias detection and masking
- Score normalization
- Fairness engine
- Testing module
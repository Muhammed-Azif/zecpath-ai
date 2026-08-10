# Zecpath AI ATS
# Developer Guide

---

## 1. Purpose

This guide explains how developers can set up, run, test, debug and
extend the Zecpath AI ATS.

---

# 2. Project Structure

The project is organized into separate layers.

```text
zecpath-ai/
│
├── ats_engine/
│   ├── scorer
│   ├── weight configuration
│   └── ATS evaluation logic
│
├── routes/
│   └── API endpoints
│
├── utils/
│   ├── skill_dictionary
│   ├── skill_normalizer
│   └── confidence_scorer
│
├── tests/
│   └── automated tests
│
├── uploads/
│   └── uploaded resumes
│
├── logs/
│   └── application logs
│
├── docs/
│   ├── ATS_TECHNICAL_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   └── DEVELOPER_GUIDE.md
│
└── requirements.txt

3. Environment Setup

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
4. Running the Application

Start the API using the project's configured application entry point.

For a FastAPI application, this commonly follows:

uvicorn <module>:app --reload

Use the actual application module configured in the project.

5. Testing

Run the automated test suite:

pytest

For verbose output:

pytest -v

Tests should verify:

Resume processing
Skill extraction
Skill normalization
Confidence scoring
ATS scoring
API behavior
Error handling
6. Testing the ATS

A typical testing sequence is:

Start the API.
Upload a valid resume.
Confirm that a processing job is created.
Check the job status.
Wait for processing to complete.
Retrieve the ATS result.
Verify individual scores.
Verify the final weighted score.
7. Common Troubleshooting
Problem: Resume upload fails

Check:

File type
File size
Upload directory
API request format
Problem: Resume text is empty

Check:

Whether the uploaded file contains extractable text.
Whether the correct text extraction method is being used.
Whether the extraction component raised an error.
Problem: Skills are not detected

Check:

Skill dictionary
Skill normalization rules
Resume text extraction
Skill extraction logic
Confidence threshold
Problem: ATS score is incorrect

Check:

Individual component scores.
Role selected for scoring.
Role-specific weights.
Default weights.
Missing values.
Final weighted calculation.

Do not debug only the final score. First inspect each component.

Problem: Job remains in processing state

Check:

Async job execution
Background task
Processing exceptions
Application logs
Job status update logic
Problem: API returns an internal server error

Check the application logs first.

Look for:

Exception type
Stack trace
Processing stage
Job identifier
Input validation errors

Avoid returning internal stack traces to API clients.

8. Logging Guidelines

Use logging for important application events.

Examples:

INFO    Resume upload started
INFO    Processing job created
INFO    Resume processing started
INFO    Skill extraction completed
INFO    ATS scoring completed
INFO    Processing job completed
ERROR   Resume processing failed

Do not log complete resumes or unnecessary personal information.

9. Adding a New Skill

To add a new supported skill:

Add the skill to the skill dictionary.
Add normalization rules if required.
Add tests.
Run the test suite.
Verify extraction using a sample resume.
10. Adding a New Scoring Component

A new scoring component should be implemented independently.

Example:

New Component
      │
      ▼
Calculate Component Score
      │
      ▼
Add Configuration Weight
      │
      ▼
Update ATS Scorer
      │
      ▼
Add Tests
      │
      ▼
Update Documentation

The new component should not unnecessarily modify unrelated modules.

11. Changing Role Weights

Role weights should be maintained in the centralized weight
configuration.

When changing weights:

Update configuration.
Verify that the total weighting is valid.
Run scoring tests.
Test at least one sample resume.
Update documentation if the behavior changes.
12. Code Change Guidelines

Before committing changes:

Write Code
   ↓
Run Tests
   ↓
Check Errors
   ↓
Review Logs
   ↓
Update Documentation
   ↓
Commit Changes

Avoid:

Hardcoded scoring values
Duplicate business logic
Scoring logic inside routes
Silent exception handling
Unnecessary global state
13. Extending the ATS

Future developers can extend the ATS by adding:

New NLP models
New skill categories
New scoring components
New role configurations
New resume formats
Additional API endpoints
Improved semantic matching

New functionality should follow the existing modular architecture.

14. Developer Checklist

Before submitting a change:

[ ] Code implemented

[ ] Unit tests added/updated

[ ] API tests updated if required

[ ] Error handling verified

[ ] Logs verified

[ ] Documentation updated

[ ] Existing tests passing

[ ] Git changes reviewed


# Zecpath AI ATS Engine
## Technical Documentation

---

## 1. Overview

The Zecpath AI Applicant Tracking System (ATS) is an automated resume
evaluation system designed to analyze resumes against job requirements.

The system performs the following major operations:

1. Resume upload
2. Resume text extraction
3. Resume parsing
4. Skill extraction
5. Skill normalization
6. Experience evaluation
7. Education evaluation
8. Semantic similarity analysis
9. Weighted ATS scoring
10. Result generation
11. Asynchronous job processing
12. Error handling and logging

The purpose of the ATS is to provide a consistent and explainable
candidate-job matching score.

---

# 2. System Objectives

The ATS is designed to be:

- Maintainable
- Explainable
- Modular
- Extensible
- Testable
- Reliable

The scoring system separates individual evaluation components so that
each component can be modified independently.

---

# 3. High-Level Processing Flow

A resume submitted to the system follows this pipeline:

Resume Upload
      |
      v
File Validation
      |
      v
Resume Text Extraction
      |
      v
Resume Parsing
      |
      v
Skill Extraction
      |
      v
Skill Normalization
      |
      v
Experience Analysis
      |
      v
Education Analysis
      |
      v
Semantic Matching
      |
      v
ATS Scoring
      |
      v
Final ATS Result

---

# 4. Core Components

## 4.1 Resume Upload

The resume upload layer accepts the candidate's resume and performs
basic validation before processing.

Responsibilities:

- Accept resume file
- Validate file type
- Validate file size
- Store uploaded file
- Create processing job
- Return job information

---

## 4.2 Resume Text Extraction

The text extraction component converts the uploaded resume into
machine-readable text.

Responsibilities:

- Read uploaded resume
- Extract text
- Handle extraction errors
- Return normalized resume text

The extracted text is passed to downstream ATS components.

---

## 4.3 Resume Parsing

The parser identifies important resume information such as:

- Skills
- Experience
- Education
- Projects
- Certifications
- Other relevant information

Parsing separates resume information into structured data that can
be processed by the scoring engine.

---

# 5. Skill Extraction

The skill extraction engine identifies technical, business and
creative skills from resume text.

The system uses:

- Skill dictionary
- Pattern matching
- NLP processing
- Skill normalization
- Confidence scoring

Example:

Input:

    Experienced in Python, FastAPI and Machine Learning.

Possible extracted skills:

    Python
    FastAPI
    Machine Learning

---

# 6. Skill Normalization

Different names may refer to the same skill.

For example:

    ML
    Machine Learning
    machine-learning

can be normalized to:

    Machine Learning

Normalization prevents duplicate or inconsistent skill matching.

---

# 7. Confidence Scoring

Skill confidence scoring helps determine how strongly a skill is
supported by the resume text.

Confidence can consider factors such as:

- Direct skill mention
- Context
- Frequency
- NLP evidence
- Matching quality

The confidence score is used to improve the reliability of extracted
skills.

---

# 8. ATS Scoring

The ATS combines multiple evaluation components into one final score.

The major scoring components are:

- Skills score
- Experience score
- Education score
- Semantic score

The final score is calculated using configurable weights.

Conceptually:

    Final Score =
        Skills Score × Skills Weight
        +
        Experience Score × Experience Weight
        +
        Education Score × Education Weight
        +
        Semantic Score × Semantic Weight

The weights are configurable according to the target role.

---

# 9. Role-Based Weight Configuration

The ATS supports configurable role-specific weights.

For example, different roles may prioritize different factors.

A technical role may place greater importance on:

    Skills
    Semantic Matching
    Experience

Another role may assign greater importance to:

    Experience
    Education
    Skills

The scoring engine retrieves role-specific weights and falls back to
default weights when a requested role is not configured.

---

# 10. ATSScorer

The ATS scoring component is responsible for calculating the final
candidate score.

Conceptual implementation:

    class ATSScorer:

        def __init__(self, role="Default"):
            self.weights = ROLE_WEIGHTS.get(
                role,
                DEFAULT_WEIGHTS
            )

        def calculate_score(
            self,
            skills_score,
            experience_score,
            education_score,
            semantic_score
        ):
            ...
            
The scorer ensures missing component values do not cause the scoring
process to fail.

For example, a missing score is treated as zero before calculation.

---

# 11. Semantic Matching

Semantic matching evaluates the relationship between the resume and
the job description beyond exact keyword matching.

This allows the ATS to identify related concepts even when the exact
same wording is not present.

Example:

Job requirement:

    Backend API development

Resume:

    Developed REST APIs using FastAPI.

Semantic matching can identify these concepts as related.

---

# 12. Asynchronous Job Processing

Resume processing may involve multiple operations and therefore is
handled through an asynchronous job workflow.

Typical flow:

    Upload Resume
          |
          v
      Create Job
          |
          v
    Process Resume
          |
          v
    Update Job Status
          |
          v
      Store Result

Possible job states include:

    pending
    processing
    completed
    failed

This prevents long-running resume processing from blocking the
initial upload request.

---

# 13. API Layer

The API layer exposes endpoints for interacting with the ATS.

Typical responsibilities include:

- Resume upload
- Job creation
- Job status checking
- Result retrieval
- Error response handling

The API layer should remain separate from the core ATS scoring logic.

This separation makes the scoring engine reusable.

---

# 14. Error Handling

The ATS uses structured error handling to prevent unexpected failures
from producing unclear responses.

Errors should:

- Be caught at the appropriate layer
- Produce meaningful messages
- Be logged
- Avoid exposing internal implementation details
- Return appropriate API responses

Common error categories include:

- Invalid file
- Unsupported file type
- Empty resume
- Parsing failure
- Processing failure
- Invalid job ID
- Internal server error

---

# 15. Logging

Logging is used to monitor ATS processing and diagnose failures.

Important events include:

- Resume upload
- Job creation
- Processing start
- Processing completion
- Processing failure
- Parsing errors
- Scoring errors

Logs should contain useful contextual information without exposing
sensitive candidate information unnecessarily.

---

# 16. Explainability

The ATS should not only return a final score.

The score should be understandable through its individual components.

Example:

    Skills Score       : 82
    Experience Score   : 75
    Education Score    : 90
    Semantic Score     : 78

These component scores are combined using the configured role weights.

This makes the ATS easier to understand, debug and improve.

---

# 17. Extensibility

The architecture allows additional scoring components to be added.

Possible future components include:

- Certification score
- Project relevance score
- Communication score
- Location matching
- Salary matching
- Industry experience
- Career progression analysis

A new component should be implemented independently and then
integrated into the scoring configuration.

---

# 18. Security Considerations

Resume files may contain sensitive candidate information.

The system should therefore:

- Validate uploaded files
- Restrict allowed file types
- Limit file size
- Avoid unnecessary storage
- Protect API endpoints
- Avoid logging sensitive resume content
- Validate job identifiers
- Sanitize user-controlled input

---

# 19. Testing Strategy

The ATS should be tested at multiple levels.

### Unit Tests

Test individual components:

- Skill extraction
- Skill normalization
- Confidence scoring
- ATS scoring
- Weight configuration

### API Tests

Test:

- Resume upload
- Job creation
- Job status
- Result retrieval
- Invalid requests
- Error responses

### Integration Tests

Test the complete pipeline:

    Upload
      ↓
    Extraction
      ↓
    Parsing
      ↓
    Skill Extraction
      ↓
    Scoring
      ↓
    Result

---

# 20. Maintenance Guidelines

When modifying the ATS:

1. Keep components modular.
2. Avoid placing scoring logic inside API routes.
3. Update tests when changing behavior.
4. Update documentation when changing architecture.
5. Keep scoring weights configurable.
6. Use consistent error handling.
7. Use logging for important processing events.
8. Avoid hardcoding role-specific behavior.

---

# 21. Conclusion

The Zecpath AI ATS is designed as a modular resume evaluation
pipeline.

Its architecture separates:

- Input handling
- Resume processing
- NLP
- Skill extraction
- Scoring
- API processing
- Error handling
- Logging

This separation makes the ATS maintainable, explainable and easier
to extend with future AI-based candidate evaluation features.
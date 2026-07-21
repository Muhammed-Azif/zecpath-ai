"""
DATA PIPELINE ARCHITECTURE

Day 7 Deliverable: AI Data Pipeline & Storage Design

This document describes how data flows through Zecpath from resume upload
to hiring decision, with clear stage boundaries and transformations.
"""

# ============================================================================
# PIPELINE OVERVIEW
# ============================================================================

"""
┌─────────────┐
│   STAGE 1   │  Candidate uploads resume (PDF/DOCX)
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────────────────────────────────────┐
│ DAY 5: Resume Text Extraction                                   │
│ INPUT:  resume.pdf / resume.docx                               │
│ LOGIC:  Extract text, clean, normalize                         │
│ OUTPUT: ResumeProfile JSON (structured candidate data)         │
└──────┬──────────────────────────────────────────────────────────┘
       │
       ↓
┌─────────────────────────────────────────────────────────────────┐
│ STORAGE: pipeline_data/candidates/{candidate_id}/              │
│          resume_raw/ + profile/                                │
│ KEEPS:   Original resume file + extracted JSON profile         │
│ VERSION: v1.0 (model_version in metadata)                      │
└──────┬──────────────────────────────────────────────────────────┘
       │
       ↓ (Resume now in system, searchable)
       │
       ├─────────────────────────────────────────────────────────┐
       │                                                           │
       ↓                                                           ↓
┌─────────────────────┐                     ┌──────────────────────┐
│ DAY 6: JD Parsing   │                     │ DAY 9: Skill Extract │
│ INPUT: raw JD text  │                     │ INPUT: Resume text   │
│ OUTPUT: JobProfile  │                     │ OUTPUT: Skills list  │
└─────────────────────┘                     │ (updates resume)     │
                                             └──────────────────────┘
       │                                            │
       ↓                                            ↓
┌──────────────────────┐                  ┌──────────────────────────┐
│ STORAGE: Jobs/       │                  │ DAY 11: Education Parse  │
│ JD parsing results   │                  │ Extract education        │
└──────────────────────┘                  │ (updates resume)         │
                                           └──────────────────────────┘
       │                                            │
       └─────────────────────────┬──────────────────┘
                                 │
                                 ↓
                    ┌─────────────────────────────────────────────┐
                    │ DAY 12: Semantic Matching                    │
                    │ Compare resume (Day 5) to JD (Day 6)        │
                    │ Using embeddings & similarity scoring       │
                    │ OUTPUT: Match score & matched skills        │
                    └────────────┬────────────────────────────────┘
                                 │
                                 ↓
                    ┌─────────────────────────────────────────────┐
                    │ DAY 13: ATS Scoring                         │
                    │ Combine all scores (skill, experience, etc) │
                    │ OUTPUT: ATSScore JSON                       │
                    └────────────┬────────────────────────────────┘
                                 │
                                 ↓
                    ┌─────────────────────────────────────────────┐
                    │ STORAGE: ats_results/{job_id}/{candidate_id}│
                    │ DECISION: SHORTLIST / REVIEW / REJECT       │
                    └────────────┬────────────────────────────────┘
                                 │
                    ┌────────────┴─────────────────┐
                    │                              │
                    ↓ (if SHORTLIST)               ↓ (if REJECT)
          ┌──────────────────────┐      ┌─────────────────────┐
          │ DAY 4 (Phase 2):     │      │ Auto-rejection      │
          │ AI Voice Screening   │      │ EMAIL               │
          │ INPUT: Candidate ID  │      └─────────────────────┘
          │ CALL: AI interviews  │
          │ OUTPUT: ScreeningRpt │
          └──────────┬───────────┘
                     │
                     ↓
          ┌──────────────────────────────────┐
          │ STORAGE: screening/               │
          │ KEEPS: Call recording + transcript│
          │ + AI assessment                  │
          └──────────┬───────────────────────┘
                     │
                     ↓
          ┌──────────────────────────────────┐
          │ DAY 11+ (Phase 2): HR Interview   │
          │ & Technical Interviews           │
          │ OUTPUT: InterviewResult JSON      │
          └──────────┬───────────────────────┘
                     │
                     ↓
          ┌──────────────────────────────────┐
          │ FINAL DECISION ENGINE             │
          │ Combine all scores                │
          │ → OFFER / HOLD / REJECT           │
          └──────────────────────────────────┘
"""


# ============================================================================
# DATA FLOW DETAIL: Resume Upload to ATS Score
# ============================================================================

"""
STEP 1: Resume Upload
─────────────────────
User: Recruiter or candidate uploads resume.pdf

Backend receives:
  - file: resume.pdf
  - candidate_id: "cand_12345"  ← Generated by backend
  - job_id: "job_67890"  ← Job they're applying for

STEP 2: Day 5 - Text Extraction
────────────────────────────────
Input to Day 5:
  {
    "file_path": "/uploads/resume.pdf",
    "candidate_id": "cand_12345"
  }

Day 5 processes:
  - Reads PDF content
  - Extracts text (handles tables, columns)
  - Cleans & normalizes

Output from Day 5:
  {
    "source_file": "resume.pdf",
    "cleaned_text": "Priya Sharma\nPython\nDjango\n...",
    "char_count": 861,
    "raw_text": "..."  (before cleaning)
  }

Stored as:
  pipeline_data/candidates/cand_12345/
  ├── resume_raw/resume.pdf  (original file)
  └── profile/profile_v1.json  (Day 5 output)

STEP 3: Day 9 - Skill Extraction
─────────────────────────────────
Input: Cleaned resume text from Step 2

Reads: "Python Django React Node.js"
Normalizes: ["Python", "Django", "React", "Node.js"]

Updates: pipeline_data/candidates/cand_12345/profile/profile_v1.json
Adds: "skills": ["Python", "Django", "React", "Node.js"]

STEP 4: Day 6 - JD Parsing (separate flow)
───────────────────────────────────────────
Input: job_description.txt for job_id "job_67890"

Output:
  {
    "role_category": "Software Engineer - Backend",
    "required_skills": ["Python", "Django", "PostgreSQL"],
    "min_years_experience": 2,
    "max_years_experience": 4
  }

Stored as:
  pipeline_data/jobs/job_67890/profile/profile_v1.json

STEP 5: Day 12 - Semantic Matching
──────────────────────────────────
Input:
  - Resume profile from Step 3: candidate_id="cand_12345"
  - JD profile from Step 4: job_id="job_67890"

Reads both JSON files, converts to embeddings, compares.

Output:
  {
    "skill_match_score": 75,  (3 out of 4 required skills match)
    "semantic_similarity": 0.82,
    "matched_skills": ["Python", "Django"],
    "missing_skills": ["PostgreSQL"]
  }

STEP 6: Day 13 - ATS Scoring
────────────────────────────
Input: Semantic matching output + resume/JD profiles

Combines:
  - Skill match (75)
  - Experience relevance (60) ← 2 years vs required 2-4
  - Education alignment (85)
  - Semantic similarity (82)

Weighted average:
  final_score = 0.3*75 + 0.3*60 + 0.2*85 + 0.2*82 = 75

Decision:
  - Score > 70 → SHORTLIST
  - Score 40-70 → REVIEW
  - Score < 40 → REJECT

Output stored as:
  pipeline_data/ats_results/job_67890/cand_12345/score_v1.json

Metadata in score:
  {
    "candidate_id": "cand_12345",
    "job_id": "job_67890",
    "model_version": "ats_v1.2.3",  ← For reproducibility
    "timestamp": 1721242000.123,    ← When score was created
    "source_system": "day13_ats_engine",
    "execution_id": "exec_abc123"    ← For tracing this run
  }
"""


# ============================================================================
# METADATA STANDARDS
# ============================================================================

"""
Every data object in the pipeline has METADATA:

Why?
  1. Reproducibility: Know which model version created this data
  2. Tracing: Debug failures by looking up execution_id
  3. Versioning: When we retrain models, old data stays tagged with old versions
  4. Audit: Track who/what/when for compliance

Every metadata object contains:

candidate_id
  - Unique ID assigned when candidate first enters system
  - Used to find all data for that candidate across all stages
  - Example: "cand_12345"

job_id
  - Unique ID for a job posting
  - Used to find all candidates considered for that job
  - Example: "job_67890"

model_version
  - Version of the AI model that created this
  - Allows rollback or comparison between versions
  - Example: "ats_v1.2.3", "semantic_match_v2.0.1"

timestamp
  - Unix epoch when data was created
  - Allows sorting and time-based queries
  - Example: 1721242000.123

source_system
  - Which day/system created this
  - Helps trace where errors come from
  - Example: "day5_resume_extractor", "day13_ats_engine"

execution_id
  - Unique ID for this single run/execution
  - If Day 13 runs on 1000 candidates, all get same execution_id
  - Allows looking up "what happened in execution exec_abc123?"
  - Example: "exec_abc123"

Example metadata object:
{
  "candidate_id": "cand_12345",
  "job_id": "job_67890",
  "model_version": "ats_v1.2.3",
  "timestamp": 1721242000.123,
  "source_system": "day13_ats_engine",
  "execution_id": "exec_abc123"
}
"""


# ============================================================================
# VERSIONING & RETRAINING
# ============================================================================

"""
Over time, AI models improve. How do we handle that?

Scenario: Day 13 ATS model goes from v1.0 to v2.0

Problem: Old data was scored with v1.0, new candidates with v2.0.
Can't compare them directly (different scales, logic).

Solution: Tag everything with model_version

Old data:
{
  "model_version": "ats_v1.0.0",
  "final_score": 75  (under v1.0 logic)
}

New data:
{
  "model_version": "ats_v2.0.0",
  "final_score": 68  (under v2.0 logic, different formula)
}

When comparing candidates:
  - Only compare v2.0 to v2.0
  - Can trace why scores changed (v1.0 to v2.0)
  - Can re-score old candidates with v2.0 if needed

Retraining dataset:
  - Gather all v1.0 scores + outcomes (hired, rejected, etc.)
  - Find patterns in what scored well vs poorly
  - Improve v2.0 model based on real outcomes
  - Test v2.0 on historical data before going live
"""


# ============================================================================
# STORAGE ORGANIZATION
# ============================================================================

"""
Directory structure keeps data organized and queryable:

By Candidate:
  pipeline_data/candidates/cand_12345/
    - All data for one candidate
    - Useful for: "Show me everything for this candidate"

By Job:
  pipeline_data/jobs/job_67890/
    - All JD data for one job
    - Useful for: "Show me this job's requirements"

By Match (ATS Result):
  pipeline_data/ats_results/job_67890/cand_12345/
    - Score for this specific candidate → job pair
    - Useful for: "How does this candidate rank for this job?"

Why this structure?
  - Clear separation of concerns
  - Fast lookups (candidate's data is in one folder)
  - Scalable (adding candidates doesn't slow other lookups)
  - Versioning (keep profile_v1, profile_v2 side by side)

Example queries:
  - "Get all candidates for job_67890":
    → ls pipeline_data/ats_results/job_67890/
  
  - "Get all scores for candidate":
    → find pipeline_data/ats_results -name cand_12345
  
  - "Compare score between model versions":
    → diff score_v1.json score_v2.json
"""

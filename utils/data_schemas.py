"""
utils/data_schemas.py

Day 7 Deliverable: Metadata standards and data entity schemas for Zecpath AI pipeline.

Defines the structure of every piece of data that flows through the system:
- Candidate profiles (from resume extraction)
- Job profiles (from JD parsing)
- ATS scores and results
- Screening reports
- Interview results

These schemas ensure consistency across Days 5-20 so downstream systems can
rely on a known, predictable data structure.
"""

from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


# ============================================================================
# METADATA STANDARDS
# ============================================================================

@dataclass
class Metadata:
    """
    Standard metadata attached to every data object.
    Tracks provenance, versioning, and timing.
    """
    candidate_id: str  # Unique ID for this candidate across the platform
    job_id: str  # Unique ID for this job posting
    model_version: str  # Which version of the AI model created this (e.g., "ats_v1.2.3")
    timestamp: float  # Unix epoch when this data was created
    source_system: str  # Which day/system created this (e.g., "day5_resume_extractor")
    execution_id: str  # Unique ID for this execution (for tracing)


# ============================================================================
# RESUME DATA SCHEMA (Output from Day 5)
# ============================================================================

@dataclass
class ResumeProfile:
    """
    Structured candidate profile extracted from resume (Day 5 output).
    This is what goes into storage after resume text extraction.
    """
    metadata: Metadata
    
    # Basic info
    candidate_name: str
    contact_email: str
    contact_phone: Optional[str]
    current_location: str
    
    # Professional summary
    raw_resume_text: str  # Original cleaned text from Day 5
    
    # Extracted fields (for downstream use)
    total_experience_years: Optional[float]
    last_company: Optional[str]
    last_job_title: Optional[str]
    
    # Lists (populated by later systems)
    skills: List[str]  # Normalized skills (from Day 9)
    education: List[str]  # Education keywords (from Day 11)
    certifications: List[str]  # Certifications found
    
    # Storage path
    resume_file_path: str  # Where the original resume is stored


# ============================================================================
# JOB DESCRIPTION DATA SCHEMA (Output from Day 6)
# ============================================================================

@dataclass
class JobProfile:
    """
    Structured job requirements extracted from JD (Day 6 output).
    This is what goes into storage after JD parsing.
    """
    metadata: Metadata
    
    # Basic info
    role_title_raw: str  # Original title from JD
    role_category: str  # Normalized (e.g., "Software Engineer - Full Stack")
    company_name: str
    
    # Requirements
    required_skills: List[str]  # Normalized skill names
    preferred_skills: List[str]
    
    # Experience requirement
    min_years_experience: Optional[int]
    max_years_experience: Optional[int]
    fresher_friendly: bool
    
    # Education requirement
    education_requirements: List[str]  # Keywords (e.g., ["b.tech", "b.e"])
    
    # Full text
    raw_jd_text: str  # Original cleaned text from Day 6


# ============================================================================
# ATS SCORING RESULT (Output from Day 13)
# ============================================================================

@dataclass
class ATSScore:
    """
    ATS scoring result - candidate's match against a specific job.
    Output after Days 12-13 (semantic matching + scoring).
    """
    metadata: Metadata
    
    # Overall score
    final_score: float  # 0-100
    percentile: float  # How candidate ranks vs. other applicants (0-100)
    
    # Component scores
    skill_match_score: float  # How many skills match
    experience_relevance_score: float  # How relevant their experience is
    education_alignment_score: float  # How aligned their education is
    semantic_similarity_score: float  # Deep semantic match (from Day 12)
    
    # Decision
    recommendation: str  # "SHORTLIST", "REVIEW", "REJECT"
    confidence: float  # Confidence in this recommendation (0-100)
    
    # Explanation
    matched_skills: List[str]  # Which skills matched
    missing_skills: List[str]  # Required skills they lack
    reasoning: str  # Human-readable explanation


# ============================================================================
# SCREENING REPORT (Output from Day 5 AI Voice Call)
# ============================================================================

@dataclass
class ScreeningReport:
    """
    Report from Day 5 AI voice screening call.
    Contains candidate responses and initial assessment.
    """
    metadata: Metadata
    
    # Call metadata
    call_timestamp: float
    call_duration_seconds: int
    call_status: str  # "COMPLETED", "MISSED", "FAILED"
    
    # Responses (from AI conversation)
    self_introduction: str
    education_mentioned: str
    total_experience_stated: str
    relevant_skills_mentioned: List[str]
    current_location_stated: str
    notice_period_days: Optional[int]
    expected_salary_range: Optional[str]
    
    # AI Assessment
    communication_clarity_score: float  # 0-100
    interest_level_score: float  # 0-100
    move_to_next_round: bool
    
    # Recording metadata
    call_recording_path: Optional[str]
    transcript_path: Optional[str]


# ============================================================================
# INTERVIEW RESULT (Output from Day 11 HR Video Interview)
# ============================================================================

@dataclass
class InterviewResult:
    """
    Result from Day 11 AI HR video interview.
    Contains answers, behavior analysis, and scoring.
    """
    metadata: Metadata
    
    # Interview metadata
    interview_type: str  # "HR", "TECHNICAL", "FINAL"
    interview_timestamp: float
    duration_seconds: int
    
    # Responses and assessments
    answers: Dict[str, str]  # question -> candidate's answer
    
    # Scoring
    communication_skills_score: float  # 0-100
    confidence_score: float  # 0-100
    aptitude_score: float  # 0-100
    behavioral_score: float  # 0-100
    
    # Behavior analysis (from Day 18)
    eye_contact_consistency: float  # 0-100
    confidence_indicators: List[str]  # ["steady_speech", "good_posture", ...]
    stress_indicators: List[str]  # ["frequent_pauses", "fidgeting", ...]
    
    # Malpractice detection (from Day 19)
    malpractice_flags: List[str]  # ["tab_switch", "external_voice", ...]
    integrity_score: float  # 0-100
    
    # Recording
    video_path: Optional[str]
    transcript_path: Optional[str]


# ============================================================================
# DATA STORAGE PATHS (Standard layout for all stored data)
# ============================================================================

class DataStoragePaths:
    """
    Standard directory structure for organizing all pipeline data.
    
    Structure:
    
    pipeline_data/
    ├── candidates/
    │   ├── <candidate_id>/
    │   │   ├── resume_raw/          # Original resume files
    │   │   │   ├── resume.pdf
    │   │   │   └── resume_extracted.json
    │   │   ├── profile/             # Extracted candidate profile
    │   │   │   └── profile_v1.json
    │   │   ├── screening/           # Screening call results
    │   │   │   ├── call_recording.wav
    │   │   │   ├── transcript.txt
    │   │   │   └── screening_report.json
    │   │   └── interviews/          # Interview results
    │   │       ├── hr_interview.json
    │   │       ├── technical_interview.json
    │   │       └── final_interview.json
    │
    ├── jobs/
    │   ├── <job_id>/
    │   │   ├── jd_raw/              # Original JD
    │   │   │   └── job_description.txt
    │   │   └── profile/             # Parsed job profile
    │   │       └── profile_v1.json
    │
    ├── ats_results/
    │   ├── <job_id>/
    │   │   └── <candidate_id>/
    │   │       └── ats_score_v1.json
    │
    └── metadata/
        └── versioning.json          # Model versions used
    """

    CANDIDATE_DIR = "pipeline_data/candidates/{candidate_id}"
    RESUME_RAW_DIR = "{candidate_dir}/resume_raw"
    CANDIDATE_PROFILE_DIR = "{candidate_dir}/profile"
    SCREENING_DIR = "{candidate_dir}/screening"
    INTERVIEWS_DIR = "{candidate_dir}/interviews"
    
    JOB_DIR = "pipeline_data/jobs/{job_id}"
    JOB_RAW_DIR = "{job_dir}/jd_raw"
    JOB_PROFILE_DIR = "{job_dir}/profile"
    
    ATS_RESULTS_DIR = "pipeline_data/ats_results/{job_id}/{candidate_id}"
    
    METADATA_DIR = "pipeline_data/metadata"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def dataclass_to_json(obj) -> str:
    """Convert a dataclass to JSON string."""
    return json.dumps(asdict(obj), default=str, indent=2)


def create_metadata(candidate_id: str, job_id: str, model_version: str, 
                   source_system: str, execution_id: str) -> Metadata:
    """Create a standard metadata object."""
    return Metadata(
        candidate_id=candidate_id,
        job_id=job_id,
        model_version=model_version,
        timestamp=datetime.now().timestamp(),
        source_system=source_system,
        execution_id=execution_id
    )

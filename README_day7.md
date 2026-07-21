# Day 7 – AI Data Pipeline & Storage Design

Defines how data flows through Zecpath from resume upload to hiring decision.

## What it does

This is **architecture and design** — no heavy coding, but critical foundation:

- **Defines data schemas**: What does resume data look like? JD data? ATS scores? Interview results?
- **Specifies metadata standards**: How do we track which model version created which data?
- **Documents the pipeline**: Shows how data flows from Day 5 → 6 → 9 → 12 → 13
- **Organizes storage**: Directory structure so data stays organized and queryable

## Files

- `utils/data_schemas.py` – Python dataclasses defining every data structure (ResumeProfile, JobProfile, ATSScore, etc.)
- `DATA_PIPELINE_ARCHITECTURE.md` – Full documentation of how data flows through the system
- `README.md` (this file)

## Key Concepts

### Metadata

Every piece of data has metadata tracking:
- `candidate_id` – Who does this data belong to?
- `job_id` – Which job is this for?
- `model_version` – Which AI model created this? (for reproducibility)
- `timestamp` – When was this created?
- `source_system` – Which day/system created this?
- `execution_id` – Unique ID for this run (for tracing)

Why? So when bugs happen or models change, you can trace exactly what went wrong.

### Storage Organization

```
pipeline_data/
├── candidates/{candidate_id}/
│   ├── resume_raw/          # Original resume file
│   ├── profile/             # Extracted resume data
│   ├── screening/           # Voice screening results
│   └── interviews/          # HR/Technical interview results
├── jobs/{job_id}/
│   ├── jd_raw/              # Original JD file
│   └── profile/             # Parsed JD data
└── ats_results/{job_id}/{candidate_id}/
    └── score_v1.json        # ATS score for this match
```

### Data Flow

```
Resume Upload (Day 5)
        ↓
Extracted & cleaned (Day 5)
        ↓
Skills added (Day 9)
        ↓
Education added (Day 11)
        ↓ (Combined with JD from Day 6)
Semantic matching (Day 12)
        ↓
ATS scoring (Day 13)
        ↓
Decision: SHORTLIST / REVIEW / REJECT
        ↓ (if SHORTLIST)
Screening call (Day 4, Phase 2)
        ↓
Interviews (Day 11+, Phase 2)
        ↓
Final decision & offer
```

## Why This Matters

Without a clear pipeline design:
- Day 5 (resume extraction) doesn't know where to store data
- Day 12 (semantic matching) doesn't know what format resume/JD data is in
- When models are retrained, old data gets mixed with new data (incorrect comparisons)
- Debugging failures becomes a nightmare (no tracing)

Day 7 solves all of that by:
1. Defining the exact structure of every data type
2. Standardizing metadata so everything is traceable
3. Organizing storage so queries are fast
4. Enabling versioning so model improvements don't break old data

## Next Steps

- Days 8-10: More extraction systems (section segmentation, skill extraction, experience parsing)
- Day 12: Use these schemas to compare resume → JD
- Day 13: Use these schemas to score matches

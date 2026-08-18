# Day 23 — Transcript Metadata Standards

## 1. Purpose

The Zecpath AI transcript architecture defines a common format
for storing voice-based HR screening conversations.

The structure allows transcript data to be processed by:

- Speech-to-text systems
- AI screening models
- Candidate evaluation systems
- ATS scoring components
- Analytics systems

---

## 2. Required Metadata

Every transcript must contain the following identifiers.

| Field | Type | Required | Description |
|---|---|---|---|
| transcript_id | string | Yes | Unique transcript identifier |
| candidate_id | string | Yes | Unique candidate identifier |
| job_id | string | Yes | Unique job identifier |
| question_id | string | Yes | Screening question identifier |
| timestamp | float | Yes | Time offset in seconds |
| confidence | float | Yes | Speech recognition confidence |

---

## 3. Candidate ID

Format:

candidate_id = `cand_<unique_id>`

Example:

`cand_001`

The candidate ID must remain consistent across:

- Resume data
- ATS scoring
- Screening questions
- Voice transcripts
- Screening results

---

## 4. Job ID

Format:

job_id = `job_<unique_id>`

Example:

`job_001`

The job ID connects the transcript to the job being evaluated.

---

## 5. Question ID

Format:

question_id = `q_<unique_id>`

Example:

`q_001`

Question IDs must correspond to the HR screening question dataset.

---

## 6. Timestamp

Timestamps represent the number of seconds from
the beginning of the voice conversation.

Example:

```text
5.2
28.4
35.1
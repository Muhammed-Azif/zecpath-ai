
# Day 24 — STT Accuracy Test Report

## 1. Objective

The objective of this test is to evaluate the Zecpath AI
speech-to-text processing pipeline under different speech
conditions and verify that transcript normalization produces
clean text suitable for AI analysis.

---

## 2. Test Environment

| Component | Configuration |
|---|---|
| Project | Zecpath AI |
| Python | Python 3.14 |
| Test Framework | pytest |
| Evaluation Metric | Word Error Rate (WER) |
| Normalization | TranscriptNormalizer |
| Processor | CleanTranscriptProcessor |

---

## 3. Test Conditions

The following conditions were evaluated:

1. Standard speech
2. Indian English accent
3. Fast speech
4. Background noise
5. Filler-heavy speech
6. Interrupted speech
7. Partial answers
8. Silence

---

## 4. Evaluation Metric

### Word Error Rate

Word Error Rate measures the difference between the
reference transcript and the STT output.

Formula:

```text
WER = (S + D + I) / N
````

Where:

* S = substitutions
* D = deletions
* I = insertions
* N = number of words in the reference transcript

A lower WER indicates better transcription accuracy.

---

## 5. Test Cases

| Test ID | Condition             | Purpose                      |
| ------- | --------------------- | ---------------------------- |
| stt_001 | Standard speech       | Baseline transcription       |
| stt_002 | Indian English accent | Accent robustness            |
| stt_003 | Fast speech           | Rapid speech handling        |
| stt_004 | Background noise      | Noise robustness             |
| stt_005 | Filler-heavy speech   | Filler removal               |
| stt_006 | Interrupted speech    | Interruption handling        |
| stt_007 | Partial answer        | Incomplete response handling |
| stt_008 | Silence               | Silence detection            |

---

## 6. Normalization Tests

The transcript normalization pipeline performs the following:

### Filler Word Removal

Examples:

```text
Um
Uh
Erm
Er
Hmm
You know
Basically
Actually
```

These are removed when they do not contribute meaningful
information to the candidate response.

---

### Case Normalization

Example:

```text
i have experience with python
```

becomes:

```text
I have experience with python.
```

---

### Punctuation Normalization

Example:

```text
I worked with Python
```

becomes:

```text
I worked with Python.
```

---

### Interrupted Speech

Example:

```text
I worked with Python - actually I worked with Python and Java
```

is converted into clean text while preserving the
candidate's intended meaning.

---

### Partial Answers

Partial responses are preserved.

The system does not invent missing information.

Example:

```text
I have experience with machine learning-
```

is cleaned without adding information that the candidate
did not provide.

---

### Silence Detection

The system recognizes:

```text
[silence]
[silent]
(silence)
[noise]
[inaudible]
[unintelligible]
```

as non-meaningful transcript output.

Silence is removed before downstream AI processing.

---

## 7. Test Execution

The evaluator can be executed using:

```text
python -m tests.stt_accuracy_evaluator
```

The evaluation generates:

* Raw WER
* Cleaned WER
* Reference transcript
* Raw STT output
* Clean transcript

for every test condition.

---

## 8. Result Interpretation

The evaluation separates two concepts:

### STT Accuracy

Raw WER measures the quality of the speech-to-text output.

### Transcript Cleaning

Cleaned WER measures the transcript after normalization.

Normalization is not considered a replacement for the
speech-to-text engine. It is a preprocessing layer that
improves consistency before AI analysis.

---

## 9. Important Limitation

The current Day 24 evaluation uses controlled reference
transcripts and representative STT outputs.

It does not claim real-world microphone accuracy.

Actual production STT accuracy must be measured using:

* Real audio recordings
* Multiple speakers
* Different accents
* Different microphones
* Background noise
* Different speaking speeds
* Real speech-to-text provider output

This prevents the system from reporting an artificial
accuracy percentage.

---

## 10. Day 24 Findings

The Zecpath AI transcript processing layer successfully
supports:

* Filler word removal
* Case normalization
* Punctuation normalization
* Interrupted speech handling
* Partial answer preservation
* Silence detection
* Clean transcript generation
* Structured STT evaluation

The normalized transcript is now suitable for downstream:

* Skill extraction
* Semantic matching
* Candidate screening
* Eligibility analysis
* ATS processing

---

## 11. Day 24 Status

| Deliverable                      | Status   |
| -------------------------------- | -------- |
| Speech-to-text service interface | Complete |
| Transcript normalization module  | Complete |
| Clean transcript processor       | Complete |
| STT accuracy evaluator           | Complete |
| STT accuracy test cases          | Complete |
| STT accuracy report              | Complete |
| Automated transcript tests       | Passed   |

---

## 12. Architecture

```text
Voice Input
    |
    v
Speech-to-Text Service
    |
    v
Raw Transcript
    |
    v
TranscriptNormalizer
    |
    +--> Filler Removal
    +--> Case Normalization
    +--> Punctuation
    +--> Interrupted Speech
    +--> Partial Answers
    +--> Silence Detection
    |
    v
CleanTranscriptProcessor
    |
    v
Clean Structured Transcript
    |
    v
AI Screening / ATS Pipeline


# Zecpath AI — Day 10: Experience Parsing & Relevance Engine

## Objective
Parse professional experience, calculate total experience without double-counting overlaps,
detect gaps/overlaps, and score relevance against a target job.

## Files
- `models.py` — structured data models
- `experience_parser.py` — experience/date parser and timeline analysis
- `relevance_engine.py` — explainable role/skill/content relevance scoring
- `day10_demo.py` — runnable example
- `test_day10.py` — basic tests

## Run

```bash
python day10_demo.py
python test_day10.py
```

## Current scoring
- Role/title similarity: 30%
- Experience-content similarity: 45%
- Skill overlap: 25%

This is intentionally an explainable baseline. In the next iteration it can be upgraded
to embedding-based semantic similarity and connected to the Zecpath resume parser/API.

# Day 6 – Job Description Parsing System

Converts raw job descriptions into structured, AI-readable job requirement objects.

## What it does

- Extracts role title and normalizes to canonical role category
- Finds and normalizes required skills (handles synonyms like "js" → "JavaScript")
- Extracts experience requirements (e.g. "2-4 years")
- Extracts education requirements (e.g. "B.Tech")
- Outputs clean structured JSON

## Usage

```python
from parsers.jd_parser import parse_jd

result = parse_jd(raw_jd_text, source_name="mern_developer.txt", output_dir="outputs/parsed")
print(result["role_category"])
print(result["required_skills"])
```

## Files

- `parsers/jd_parser.py` – Core parser
- `utils/skill_synonyms.py` – Skill mapping & normalization
- `tests/test_jd_parser.py` – Automated tests
- `data/sample_jds/` – Sample job descriptions

## Run tests

```bash
python tests\test_jd_parser.py
```

Should show `3/3 passed`.
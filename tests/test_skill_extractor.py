"""
Day 9 - Skill Extraction Engine Tests

Tests:
1. Technical skill extraction
2. Business skill extraction
3. Creative skill extraction
4. Skill synonyms
5. Skill stack expansion
6. Deduplication and normalization
7. Confidence scoring
8. Structured output
"""

from parsers.skill_extractor import SkillExtractor
import json
from pathlib import Path

def get_skill_names(results):
    return {item["skill"] for item in results}


def test_technical_skills():
    text = """
    Technical Skills:
    Python, JavaScript, SQL, React, Docker
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    skills = get_skill_names(results)

    expected = {
        "Python",
        "JavaScript",
        "SQL",
        "React",
        "Docker"
    }

    assert expected.issubset(skills)

    print("[PASS] Technical skill extraction")


def test_business_skills():
    text = """
    Business Skills:
    Project Management, Agile, Scrum, Leadership
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    skills = get_skill_names(results)

    expected = {
        "Project Management",
        "Agile",
        "Scrum",
        "Leadership"
    }

    assert expected.issubset(skills)

    print("[PASS] Business skill extraction")


def test_creative_skills():
    text = """
    Creative Skills:
    Figma, Canva, Graphic Design, UI Design
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    skills = get_skill_names(results)

    expected = {
        "Figma",
        "Canva",
        "Graphic Design",
        "UI Design"
    }

    assert expected.issubset(skills)

    print("[PASS] Creative skill extraction")


def test_skill_synonyms():
    text = """
    Skills:
    Py, JS, ReactJS, Node, ML, AI
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    skills = get_skill_names(results)

    expected = {
        "Python",
        "JavaScript",
        "React",
        "Node.js",
        "Machine Learning",
        "Artificial Intelligence"
    }

    assert expected.issubset(skills)

    print("[PASS] Skill synonym normalization")


def test_skill_stack_mern():
    text = """
    Full Stack Developer
    MERN
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    skills = get_skill_names(results)

    expected = {
        "MongoDB",
        "Express.js",
        "React",
        "Node.js"
    }

    assert expected.issubset(skills)

    print("[PASS] MERN stack expansion")


def test_skill_stack_mean():
    text = """
    Full Stack Developer
    MEAN
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    skills = get_skill_names(results)

    expected = {
        "MongoDB",
        "Express.js",
        "Angular",
        "Node.js"
    }

    assert expected.issubset(skills)

    print("[PASS] MEAN stack expansion")


def test_deduplication():
    text = """
    Python
    python
    PYTHON
    Py
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    skills = [
        item["skill"]
        for item in results
    ]

    assert skills.count("Python") == 1

    print("[PASS] Skill deduplication")


def test_confidence_scores():
    text = """
    Python JavaScript ReactJS MERN
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    assert len(results) > 0

    for item in results:

        assert "confidence" in item

        assert 0.0 <= item["confidence"] <= 1.0

        assert "detection_methods" in item

    print("[PASS] Confidence scoring")


def test_structured_output():
    text = """
    Python
    ReactJS
    """

    extractor = SkillExtractor()
    results = extractor.extract(text)

    assert isinstance(results, list)

    for item in results:

        assert "skill" in item
        assert "category" in item
        assert "confidence" in item
        assert "detection_methods" in item

    print("[PASS] Structured skill output")

def generate_skill_output():
    """
    Generate a structured JSON skill extraction result
    for Day 9 deliverables.
    """

    sample_resume = """
    Muhammed is a software developer with experience in
    Python, JavaScript, ReactJS, and the MERN stack.

    Business skills include Project Management, Agile,
    Scrum, and Leadership.

    Creative skills include Figma, Canva, and UI Design.
    """

    extractor = SkillExtractor()
    results = extractor.extract(sample_resume)

    output = {
        "document": "day9_sample_resume",
        "skills": results,
        "total_skills": len(results)
    }

    output_dir = Path("outputs/skills")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "extracted_skills.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\n[OUTPUT] Structured skills written to: {output_file}")


if __name__ == "__main__":

    tests = [
        test_technical_skills,
        test_business_skills,
        test_creative_skills,
        test_skill_synonyms,
        test_skill_stack_mern,
        test_skill_stack_mean,
        test_deduplication,
        test_confidence_scores,
        test_structured_output
    ]

    passed = 0

    print("\n========================================")
    print("DAY 9 - SKILL EXTRACTION TEST")
    print("========================================\n")

    for test in tests:

        try:
            test()
            passed += 1

        except AssertionError as error:
            print(f"[FAIL] {test.__name__}")
            print(error)

        except Exception as error:
            print(f"[ERROR] {test.__name__}: {error}")

    total = len(tests)

    print("\n========================================")
    print(f"RESULT: {passed}/{total} tests passed")
    print("========================================")
    generate_skill_output()
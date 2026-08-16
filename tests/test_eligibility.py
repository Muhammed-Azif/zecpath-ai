from eligibility.eligibility_engine import EligibilityDecisionEngine


def create_engine():
    return EligibilityDecisionEngine(
        role="AI/ML Engineer"
    )


def test_eligible_candidate():
    engine = create_engine()

    candidate = {
        "candidate_id": "cand_001",
        "job_id": "job_001",
        "ats_score": 85,
        "skills": [
            "Python",
            "Machine Learning"
        ],
        "experience_years": 2,
        "location": "Trivandrum",
        "available": True
    }

    result = engine.evaluate(candidate)

    assert result["decision"] == "Eligible"


def test_review_candidate():
    engine = create_engine()

    candidate = {
        "candidate_id": "cand_002",
        "job_id": "job_001",
        "ats_score": 62,
        "skills": [
            "Python",
            "Machine Learning"
        ],
        "experience_years": 2,
        "location": "Trivandrum",
        "available": True
    }

    result = engine.evaluate(candidate)

    assert result["decision"] == "Review"


def test_rejected_low_ats_score():
    engine = create_engine()

    candidate = {
        "candidate_id": "cand_003",
        "job_id": "job_001",
        "ats_score": 40,
        "skills": [
            "Python",
            "Machine Learning"
        ],
        "experience_years": 2,
        "location": "Trivandrum",
        "available": True
    }

    result = engine.evaluate(candidate)

    assert result["decision"] == "Rejected"


def test_rejected_missing_mandatory_skill():
    engine = create_engine()

    candidate = {
        "candidate_id": "cand_004",
        "job_id": "job_001",
        "ats_score": 85,
        "skills": [
            "Python"
        ],
        "experience_years": 2,
        "location": "Trivandrum",
        "available": True
    }

    result = engine.evaluate(candidate)

    assert result["decision"] == "Rejected"


def test_review_invalid_location():
    engine = create_engine()

    candidate = {
        "candidate_id": "cand_005",
        "job_id": "job_001",
        "ats_score": 85,
        "skills": [
            "Python",
            "Machine Learning"
        ],
        "experience_years": 2,
        "location": "Mumbai",
        "available": True
    }

    result = engine.evaluate(candidate)

    assert result["decision"] == "Review"
"""
Day 13 - ATS Weight Configuration
"""

ROLE_WEIGHTS = {

    "AI/ML Engineer": {
        "skills": 0.40,
        "experience": 0.25,
        "education": 0.10,
        "semantic": 0.25
    },

    "Data Analyst": {
        "skills": 0.35,
        "experience": 0.30,
        "education": 0.10,
        "semantic": 0.25
    },

    "Backend Developer": {
        "skills": 0.45,
        "experience": 0.25,
        "education": 0.10,
        "semantic": 0.20
    },

    "Frontend Developer": {
        "skills": 0.45,
        "experience": 0.20,
        "education": 0.10,
        "semantic": 0.25
    }

}

DEFAULT_WEIGHTS = {
    "skills": 0.40,
    "experience": 0.25,
    "education": 0.10,
    "semantic": 0.25
}
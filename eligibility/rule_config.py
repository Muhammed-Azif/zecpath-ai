"""
Day 21 - Eligibility Rule Configuration

Defines configurable eligibility rules for different job roles.
"""

ROLE_ELIGIBILITY_RULES = {

    "AI/ML Engineer": {
        "minimum_ats_score": 70,
        "review_score": 55,

        "mandatory_skills": [
            "Python",
            "Machine Learning"
        ],

        "minimum_experience": 1,
        "maximum_experience": 5,

        "allowed_locations": [
            "Trivandrum",
            "Thiruvananthapuram",
            "Bangalore",
            "Bengaluru",
            "Remote"
        ],

        "availability_required": True
    },

    "Default": {
        "minimum_ats_score": 70,
        "review_score": 50,

        "mandatory_skills": [],

        "minimum_experience": 0,
        "maximum_experience": 50,

        "allowed_locations": [],

        "availability_required": False
    }
}


def get_rules(role):
    """
    Return eligibility rules for a given job role.
    Falls back to Default when role is not configured.
    """
    return ROLE_ELIGIBILITY_RULES.get(
        role,
        ROLE_ELIGIBILITY_RULES["Default"]
    )
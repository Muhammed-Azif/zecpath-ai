"""
Zecpath AI - Day 22
HR Screening Question Category Mapping
"""

QUESTION_CATEGORIES = {
    "Introduction": {
        "description": "Basic candidate introduction and motivation",
        "priority": 3
    },

    "Education": {
        "description": "Educational background and qualifications",
        "priority": 2
    },

    "Experience": {
        "description": "Professional experience and career history",
        "priority": 5
    },

    "Skills": {
        "description": "Technical and professional skills",
        "priority": 5
    },

    "Location": {
        "description": "Candidate location, relocation and work arrangement",
        "priority": 4
    },

    "Salary": {
        "description": "Compensation expectations and flexibility",
        "priority": 4
    },

    "Notice Period": {
        "description": "Availability and joining timeline",
        "priority": 5
    }
}


def get_category_mapping():
    """Return all HR screening question categories."""
    return QUESTION_CATEGORIES


def get_category_priority(category):
    """Return priority for a category."""
    category_data = QUESTION_CATEGORIES.get(category)

    if category_data is None:
        return 0

    return category_data["priority"]
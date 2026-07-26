"""
Day 9 - Master Skill Dictionary

Contains technical, business, and creative skills,
along with synonyms and skill-stack expansions.
"""

# ============================================================
# MASTER SKILL DICTIONARY
# ============================================================

SKILL_DICTIONARY = {
    "technical": {
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "C",
        "C++",
        "C#",
        "SQL",
        "HTML",
        "CSS",
        "React",
        "Angular",
        "Vue.js",
        "Node.js",
        "Express.js",
        "Django",
        "Flask",
        "FastAPI",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "Git",
        "GitHub",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "Google Cloud",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Natural Language Processing",
        "Computer Vision",
        "TensorFlow",
        "PyTorch",
        "scikit-learn",
        "Pandas",
        "NumPy",
        "Power BI",
        "Tableau",
        "REST API",
        "GraphQL",
        "Linux",
    },

    "business": {
        "Project Management",
        "Product Management",
        "Business Analysis",
        "Business Development",
        "Digital Marketing",
        "Marketing",
        "Sales",
        "Customer Relationship Management",
        "CRM",
        "Agile",
        "Scrum",
        "Leadership",
        "Communication",
        "Negotiation",
        "Team Management",
    },

    "creative": {
        "Figma",
        "Adobe Photoshop",
        "Adobe Illustrator",
        "Canva",
        "UI Design",
        "UX Design",
        "Graphic Design",
        "Video Editing",
        "Content Creation",
        "Content Writing",
    }
}


# ============================================================
# SYNONYMS / ALTERNATIVE NAMES
# ============================================================

SKILL_SYNONYMS = {
    "py": "Python",
    "python3": "Python",

    "js": "JavaScript",
    "javascript": "JavaScript",

    "ts": "TypeScript",
    "typescript": "TypeScript",

    "reactjs": "React",
    "react.js": "React",

    "angularjs": "Angular",
    "angular.js": "Angular",

    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    "express": "Express.js",
    "expressjs": "Express.js",

    "mongo": "MongoDB",
    "mongodb": "MongoDB",

    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "ml": "Machine Learning",
    "machine learning": "Machine Learning",

    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",

    "nlp": "Natural Language Processing",

    "cv": "Computer Vision",

    "powerbi": "Power BI",
    "power bi": "Power BI",

    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",

    "photoshop": "Adobe Photoshop",
    "illustrator": "Adobe Illustrator",
}


# ============================================================
# SKILL STACKS
# ============================================================

SKILL_STACKS = {
    "MERN": [
        "MongoDB",
        "Express.js",
        "React",
        "Node.js",
    ],

    "MEAN": [
        "MongoDB",
        "Express.js",
        "Angular",
        "Node.js",
    ],

    "MEVN": [
        "MongoDB",
        "Express.js",
        "Vue.js",
        "Node.js",
    ],

    "LAMP": [
        "Linux",
        "Apache",
        "MySQL",
        "PHP",
    ],
}


def get_all_skills():
    """Return all master skills as one set."""
    skills = set()

    for category_skills in SKILL_DICTIONARY.values():
        skills.update(category_skills)

    return skills


def get_skill_category(skill):
    """Return the category of a skill."""
    for category, skills in SKILL_DICTIONARY.items():
        if skill in skills:
            return category

    return "other"
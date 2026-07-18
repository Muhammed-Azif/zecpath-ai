"""
utils/skill_synonyms.py

Skill-synonym and role-variation normalization for the JD Parsing System (Day 6).

This is intentionally a plain, editable data file (not a database) so
recruiters/engineers can extend the dictionary without touching parser logic.
Day 9 (Skill Extraction Engine) and Day 12 (Semantic Matching) will reuse
this same canonical mapping so a skill is scored consistently everywhere.
"""

import re

# canonical_skill -> [accepted synonym / variant spellings]
SKILL_SYNONYMS = {
    "JavaScript": ["js", "javascript", "java script", "ecmascript"],
    "TypeScript": ["ts", "typescript"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node", "node.js", "nodejs"],
    "Express.js": ["express", "express.js", "expressjs"],
    "MongoDB": ["mongo", "mongodb"],
    "MERN Stack": ["mern", "mern stack"],
    "MEAN Stack": ["mean", "mean stack"],
    "Angular": ["angular", "angular.js", "angularjs"],
    "Vue.js": ["vue", "vue.js", "vuejs"],
    "Python": ["python", "py"],
    "Django": ["django"],
    "FastAPI": ["fastapi", "fast api"],
    "Flask": ["flask"],
    "Java": ["java"],
    "Spring Boot": ["spring", "spring boot", "springboot"],
    "SQL": ["sql", "structured query language"],
    "PostgreSQL": ["postgres", "postgresql"],
    "MySQL": ["mysql"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["k8s", "kubernetes"],
    "Git": ["git", "github", "version control"],
    "REST API": ["rest", "rest api", "restful", "restful api"],
    "GraphQL": ["graphql"],
    "CI/CD": ["ci/cd", "cicd", "continuous integration", "continuous deployment"],
    "HTML/CSS": ["html", "css", "html/css", "html5", "css3"],
    "Figma": ["figma"],
    "Adobe XD": ["adobe xd", "xd"],
    "UI/UX Design": ["ui/ux", "ui ux", "user interface design", "user experience design"],
    "Wireframing": ["wireframe", "wireframing", "wireframes"],
    "Prototyping": ["prototype", "prototyping"],
    "CRM Software": ["crm", "customer relationship management"],
    "Salesforce": ["salesforce", "sfdc"],
    "Lead Generation": ["lead gen", "lead generation"],
    "Negotiation": ["negotiation", "negotiating"],
    "Cold Calling": ["cold call", "cold calling"],
    "Communication Skills": ["communication", "communication skills", "verbal communication"],
    "Excel": ["excel", "ms excel", "microsoft excel"],
}

# role_title (free text, as written in a JD) -> canonical role category
ROLE_CATEGORY_MAP = {
    "mern stack developer": "Software Engineer - Full Stack",
    "full stack developer": "Software Engineer - Full Stack",
    "backend developer": "Software Engineer - Backend",
    "backend engineer": "Software Engineer - Backend",
    "frontend developer": "Software Engineer - Frontend",
    "frontend engineer": "Software Engineer - Frontend",
    "software engineer": "Software Engineer",
    "software developer": "Software Engineer",
    "sde": "Software Engineer",
    "ui/ux designer": "Design - UI/UX",
    "ux designer": "Design - UI/UX",
    "ui designer": "Design - UI/UX",
    "product designer": "Design - UI/UX",
    "sales executive": "Sales",
    "sales representative": "Sales",
    "business development executive": "Sales",
    "bde": "Sales",
}


def _build_reverse_index():
    index = {}
    for canonical, variants in SKILL_SYNONYMS.items():
        for v in variants:
            index[v.lower()] = canonical
        index[canonical.lower()] = canonical
    return index


_SKILL_REVERSE_INDEX = _build_reverse_index()


def normalize_skill(raw_skill: str) -> str:
    """
    Map a raw skill mention to its canonical form.
    Falls back to a title-cased version of the input if no mapping exists,
    so unknown-but-real skills aren't silently dropped.
    """
    key = raw_skill.strip().lower()
    key = re.sub(r"[.\-]", "", key) if key.replace(".", "").replace("-", "") in _SKILL_REVERSE_INDEX else key
    if key in _SKILL_REVERSE_INDEX:
        return _SKILL_REVERSE_INDEX[key]
    # try a looser match: strip punctuation only, don't collapse dots (e.g. "node.js")
    loose_key = raw_skill.strip().lower()
    if loose_key in _SKILL_REVERSE_INDEX:
        return _SKILL_REVERSE_INDEX[loose_key]
    return raw_skill.strip()


def normalize_role(raw_role: str) -> str:
    """Map a free-text job title to a canonical role category."""
    key = raw_role.strip().lower()
    if key in ROLE_CATEGORY_MAP:
        return ROLE_CATEGORY_MAP[key]
    # loose contains-match for titles like "Senior MERN Stack Developer"
    for phrase, category in ROLE_CATEGORY_MAP.items():
        if phrase in key:
            return category
    return raw_role.strip().title()


def known_skill_phrases():
    """All known skill variant phrases, longest-first (for greedy text matching)."""
    phrases = set(_SKILL_REVERSE_INDEX.keys())
    return sorted(phrases, key=len, reverse=True)

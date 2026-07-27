from parsers.experience_parser import ExperienceParser
from scoring.experience_relevance import ExperienceRelevance

text = """
Sales Officer
Apis India Ltd
Feb 2025 - Present

Sales Officer
Global Green Company
May 2023 - Jan 2025

Sales Executive
Seaberry Foods Pvt Ltd
Sep 2022 - Apr 2023
"""

parser = ExperienceParser()

jobs = parser.parse_experience(text)

engine = ExperienceRelevance()

result = engine.calculate_relevance(
    jobs,
    "Business Analyst",
    """
SQL
Excel
Communication
Sales
Reporting
"""
)

print(result)

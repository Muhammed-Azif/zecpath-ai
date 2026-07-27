from parsers.experience_parser import ExperienceParser

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

result = parser.parse_experience(text)
summary = parser.calculate_total_experience(result)
gaps = parser.detect_career_gaps(result)
overlaps = parser.detect_overlaps(result)
actual = parser.calculate_actual_experience(result)

print("\nActual Experience")
print(actual)

print("\nOverlapping Jobs")
print(overlaps)
print("\nCareer Gaps")
print(gaps)
print("\nTotal Experience")
print(summary)

for job in result:
    print(job)
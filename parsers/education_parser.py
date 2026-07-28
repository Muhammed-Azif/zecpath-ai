"""
Day 11 - Education & Certification Parser
"""

import re
class EducationParser:
    """
    Extracts education and certification details
    from resume sections.
    """

    def __init__(self):

        # Supported degree names
        self.degree_patterns = {
            "B.Tech": [
                "b.tech",
                "b tech",
                "bachelor of technology"
            ],

            "B.E.": [
                "b.e",
                "be",
                "bachelor of engineering"
            ],

            "M.Tech": [
                "m.tech",
                "master of technology"
            ],

            "MCA": [
                "mca",
                "master of computer applications"
            ],

            "BCA": [
                "bca",
                "bachelor of computer applications"
            ],

            "MBA": [
                "mba",
                "master of business administration"
            ]
        }

    def normalize_degree(self, text):
        """
        Converts different degree names into a standard format.

        Example:
            Bachelor of Technology -> B.Tech
            B Tech -> B.Tech
            BE -> B.E.
        """

        text = text.lower()

        for standard_degree, patterns in self.degree_patterns.items():

            for pattern in patterns:

                if pattern in text:
                    return standard_degree

        return None

    def parse_education(self, education_text):
        """
        Parses the Education section and returns
        structured education information.
        """

        education_list = []

        # Split into blocks (each education separated by blank line)
        blocks = education_text.strip().split("\n\n")

        for block in blocks:

            lines = [line.strip() for line in block.split("\n") if line.strip()]

            if len(lines) < 2:
                continue

            degree_line = lines[0]
            institution = lines[1]

            degree = self.normalize_degree(degree_line)

            # Extract graduation year
            year_match = re.search(r"(19|20)\d{2}", block)

            graduation_year = (
                year_match.group()
                if year_match
                else None
            )

            # Extract field of study
            field = None

            if "computer science" in degree_line.lower():
                field = "Computer Science"

            elif "information technology" in degree_line.lower():
                field = "Information Technology"

            elif "mechanical" in degree_line.lower():
                field = "Mechanical Engineering"

            elif "electronics" in degree_line.lower():
                field = "Electronics"

            education = {
                "degree": degree,
                "field": field,
                "institution": institution,
                "graduation_year": graduation_year
            }

            education_list.append(education)

        return education_list


    def parse_certifications(self, certification_text):
        """
        Parses the Certifications section and returns
        structured certification information.
        """

        certifications = []

        # Simple category mapping
        categories = {
            "machine learning": "AI/ML",
            "data science": "Data Science",
            "python": "Programming",
            "aws": "Cloud",
            "azure": "Cloud",
            "google data analytics": "Data Analytics",
            "tensorflow": "AI/ML",
            "ccna": "Networking"
        }

        lines = [
            line.strip()
            for line in certification_text.split("\n")
            if line.strip()
        ]

        for line in lines:

            category = "Other"

            lower_line = line.lower()

            for keyword, value in categories.items():

                if keyword in lower_line:
                    category = value
                    break

            year_match = re.search(r"(19|20)\d{2}", line)

            year = year_match.group() if year_match else None

            certification = {
                "name": line,
                "category": category,
                "year": year
            }

            certifications.append(certification)

        return certifications

    def build_academic_profile(self, education_text, certification_text):
        """
        Builds a structured academic profile containing
        education and certifications.
        """

        education = self.parse_education(education_text)

        certifications = self.parse_certifications(certification_text)

        profile = {
            "education": education,
            "certifications": certifications
        }

        return profile



if __name__ == "__main__":

    parser = EducationParser()

    education_text = """
Bachelor of Technology in Computer Science
University College of Engineering Kariavattom
2026
"""

    certification_text = """
Google Data Analytics Professional Certificate - 2024
AWS Cloud Practitioner
Machine Learning with Python - Coursera
"""

    profile = parser.build_academic_profile(
        education_text,
        certification_text
    )

    print(profile)
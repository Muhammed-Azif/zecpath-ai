"""
Day 11 - Education Relevance Scoring
"""

import re


class EducationRelevance:

    def extract_keywords(self, text):
        """Extract keywords from job requirements."""

        text = text.lower()

        words = re.findall(r"\b[a-zA-Z]+\b", text)

        stop_words = {
            "the", "and", "for", "with",
            "to", "of", "in", "a", "an",
            "is", "are", "required", "preferred"
        }

        return {
            word
            for word in words
            if word not in stop_words
        }

    def calculate_relevance(
        self,
        academic_profile,
        job_requirements
    ):
        """
        Calculates education relevance against
        job requirements.
        """

        candidate_text = ""

        # Add education information
        for education in academic_profile.get("education", []):

            candidate_text += " "
            candidate_text += education.get("degree", "")
            candidate_text += " "
            candidate_text += education.get("field", "")
            candidate_text += " "
            candidate_text += education.get("institution", "")

        # Add certification information
        for certification in academic_profile.get(
            "certifications", []
        ):

            candidate_text += " "
            candidate_text += certification.get("name", "")
            candidate_text += " "
            candidate_text += certification.get("category", "")

        candidate_keywords = self.extract_keywords(
            candidate_text
        )

        required_keywords = self.extract_keywords(
            job_requirements
        )

        matched = candidate_keywords & required_keywords
        missing = required_keywords - candidate_keywords

        if not required_keywords:
            score = 0
        else:
            score = round(
                len(matched) /
                len(required_keywords) *
                100,
                2
            )

        return {
            "education_score": score,
            "matched_keywords": sorted(matched),
            "missing_keywords": sorted(missing)
        }


if __name__ == "__main__":

    profile = {
        "education": [
            {
                "degree": "B.Tech",
                "field": "Computer Science",
                "institution": "University College of Engineering Kariavattom",
                "graduation_year": "2026"
            }
        ],
        "certifications": [
            {
                "name": "Machine Learning with Python",
                "category": "AI/ML",
                "year": "2025"
            }
        ]
    }

    job_requirements = """
    B.Tech Computer Science
    Python
    Machine Learning
    Data Science
    """

    scorer = EducationRelevance()

    result = scorer.calculate_relevance(
        profile,
        job_requirements
    )

    print(result)
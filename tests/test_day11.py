from parsers.education_parser import EducationParser
from scoring.education_relevance import EducationRelevance


def main():

    print("=" * 60)
    print("DAY 11 - EDUCATION & CERTIFICATION PARSING")
    print("=" * 60)

    parser = EducationParser()

    education_text = """
Bachelor of Technology in Computer Science
University College of Engineering Kariavattom
2026
"""

    certification_text = """
Machine Learning with Python - Coursera - 2025
Google Data Analytics Professional Certificate - 2024
"""

    # 1. Education parsing
    education = parser.parse_education(
        education_text
    )

    print("\n1. EDUCATION")
    print(education)

    # 2. Certification parsing
    certifications = parser.parse_certifications(
        certification_text
    )

    print("\n2. CERTIFICATIONS")
    print(certifications)

    # 3. Structured Academic Profile
    profile = parser.build_academic_profile(
        education_text,
        certification_text
    )

    print("\n3. STRUCTURED ACADEMIC PROFILE")
    print(profile)

    # 4. Education relevance
    scorer = EducationRelevance()

    job_requirements = """
    B.Tech Computer Science
    Python
    Machine Learning
    Data Science
    """

    result = scorer.calculate_relevance(
        profile,
        job_requirements
    )

    print("\n4. EDUCATION RELEVANCE")
    print(result)

    print("\n" + "=" * 60)
    print("DAY 11 TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
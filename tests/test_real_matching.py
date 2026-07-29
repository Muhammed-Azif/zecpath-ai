from semantic_matching.resume_matcher import ResumeJobMatcher


def main():

    # =====================================================
    # CHANGE THESE TWO VALUES
    # =====================================================

    resume_path = r"D:\ZECPATH-AI\data\sample_resumes\priya_sharma_resume.pdf"

    job_description = """
    AI/ML Engineer

    We are looking for an AI/ML Engineer to build and
    deploy machine learning solutions.

    Required Skills:
    Python, Machine Learning, Artificial Intelligence,
    NLP, SQL, Scikit-learn, Data Analysis.

    Responsibilities:
    Develop machine learning models.
    Perform data preprocessing and analysis.
    Build NLP applications.
    Create predictive systems using Python.
    Automate machine learning workflows.

    Experience:
    Experience with Python and machine learning projects.
    Knowledge of NLP, data analysis and AI systems.

    Education:
    Bachelor's degree in Computer Science,
    Artificial Intelligence, Data Science or related field.
    """

    # =====================================================
    # START MATCHER
    # =====================================================

    matcher = ResumeJobMatcher()

    result = matcher.match(
        resume_path,
        job_description
    )

    scores = result["scores"]

    print("\n")
    print("=" * 55)
    print("          ZECpath AI SEMANTIC MATCH")
    print("=" * 55)

    print(
        f"Skills Similarity     : "
        f"{scores['skills_score']:.2f}%"
    )

    print(
        f"Experience Similarity : "
        f"{scores['experience_score']:.2f}%"
    )

    print(
        f"Projects Similarity   : "
        f"{scores['projects_score']:.2f}%"
    )

    print("-" * 55)

    print(
        f"Final Match Score     : "
        f"{scores['final_score']:.2f}%"
    )

    print(
        f"Classification         : "
        f"{scores['classification']}"
    )

    print("=" * 55)


if __name__ == "__main__":
    main()
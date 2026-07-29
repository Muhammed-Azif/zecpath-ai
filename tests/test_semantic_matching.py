from semantic_matching.semantic_matcher import SemanticMatcher
from semantic_matching.similarity_scorer import SimilarityScorer


def main():

    matcher = SemanticMatcher()
    scorer = SimilarityScorer()

    # ==========================================
    # RESUME SECTIONS
    # ==========================================

    resume_skills = """
    Python, Machine Learning, Artificial Intelligence,
    NLP, SQL, Data Analysis, Scikit-learn,
    automation and data preprocessing.
    """

    resume_experience = """
    Worked on machine learning projects involving
    data preprocessing, model training, classification
    and prediction. Experience with Python programming,
    data analysis and automation.
    """

    resume_projects = """
    Developed machine learning projects for prediction
    and classification. Built NLP applications and
    automation solutions using Python.
    """

    # ==========================================
    # JOB DESCRIPTION SECTIONS
    # ==========================================

    job_skills = """
    Python, Machine Learning, Artificial Intelligence,
    NLP, SQL, Data Science, Scikit-learn,
    automation and data preprocessing.
    """

    job_experience = """
    The candidate will develop machine learning models,
    perform data preprocessing, train predictive models
    and build automated AI solutions.
    """

    job_projects = """
    Experience developing machine learning and NLP
    projects using Python. Candidates should be able
    to create intelligent automation solutions.
    """

    # ==========================================
    # CREATE EMBEDDINGS
    # ==========================================

    skills_resume_embedding = matcher.create_embedding(
        resume_skills
    )

    skills_job_embedding = matcher.create_embedding(
        job_skills
    )

    experience_resume_embedding = matcher.create_embedding(
        resume_experience
    )

    experience_job_embedding = matcher.create_embedding(
        job_experience
    )

    projects_resume_embedding = matcher.create_embedding(
        resume_projects
    )

    projects_job_embedding = matcher.create_embedding(
        job_projects
    )

    # ==========================================
    # CALCULATE SECTION SIMILARITIES
    # ==========================================

    skills_score = scorer.calculate_similarity(
        skills_resume_embedding,
        skills_job_embedding
    )

    experience_score = scorer.calculate_similarity(
        experience_resume_embedding,
        experience_job_embedding
    )

    projects_score = scorer.calculate_similarity(
        projects_resume_embedding,
        projects_job_embedding
    )

    # ==========================================
    # FINAL WEIGHTED SCORE
    # ==========================================

    final_score = scorer.calculate_weighted_score(
        skills_score,
        experience_score,
        projects_score
    )

    # ==========================================
    # CONVERT TO PERCENTAGE
    # ==========================================

    skills_percentage = scorer.to_percentage(
        skills_score
    )

    experience_percentage = scorer.to_percentage(
        experience_score
    )

    projects_percentage = scorer.to_percentage(
        projects_score
    )

    final_percentage = scorer.to_percentage(
        final_score
    )

    # ==========================================
    # CLASSIFICATION
    # ==========================================

    classification = scorer.classify_match(
        final_percentage
    )

    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    print("\n")
    print("=" * 50)
    print("          ZECpath AI SEMANTIC MATCH")
    print("=" * 50)

    print(f"Skills Similarity      : {skills_percentage}%")
    print(f"Experience Similarity  : {experience_percentage}%")
    print(f"Projects Similarity    : {projects_percentage}%")

    print("-" * 50)

    print(f"Final Match Score      : {final_percentage}%")
    print(f"Classification         : {classification}")

    print("=" * 50)


if __name__ == "__main__":
    main()
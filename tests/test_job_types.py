from semantic_matching.semantic_matcher import SemanticMatcher
from semantic_matching.similarity_scorer import SimilarityScorer
import pandas as pd
from pathlib import Path


def main():

    matcher = SemanticMatcher()
    scorer = SimilarityScorer()

    # =====================================================
    # CANDIDATE RESUME
    # =====================================================

    resume = {
        "skills": """
        Python, Machine Learning, Artificial Intelligence,
        NLP, SQL, Data Analysis, Scikit-learn,
        automation and data preprocessing.
        """,

        "experience": """
        Worked on machine learning projects involving
        data preprocessing, model training, classification
        and prediction. Experience with Python programming,
        data analysis and automation.
        """,

        "projects": """
        Developed machine learning projects for prediction
        and classification. Built NLP applications and
        automation solutions using Python.
        """
    }

    # =====================================================
    # JOB DESCRIPTIONS
    # =====================================================

    jobs = {

        "AI/ML Engineer": {
            "skills": """
            Python, Machine Learning, Artificial Intelligence,
            NLP, Deep Learning, Scikit-learn,
            data preprocessing and automation.
            """,

            "experience": """
            Develop machine learning models, perform
            data preprocessing, train predictive models
            and build intelligent AI solutions.
            """,

            "projects": """
            Build machine learning, NLP and artificial
            intelligence projects using Python.
            """
        },

        "Data Analyst": {
            "skills": """
            Python, SQL, Data Analysis, Statistics,
            Excel, data visualization and reporting.
            """,

            "experience": """
            Analyze datasets, clean data, perform
            statistical analysis and create reports
            to support business decisions.
            """,

            "projects": """
            Build data analysis projects involving
            Python, SQL, visualization and statistical
            analysis.
            """
        },

        "Backend Developer": {
            "skills": """
            Python, REST APIs, databases, backend
            development, SQL and server-side programming.
            """,

            "experience": """
            Develop backend applications, REST APIs,
            database systems and server-side services.
            """,

            "projects": """
            Build backend applications using Python,
            APIs, databases and server-side technologies.
            """
        },

        "Frontend Developer": {
            "skills": """
            HTML, CSS, JavaScript, React, responsive
            web design and frontend development.
            """,

            "experience": """
            Develop responsive web interfaces,
            frontend applications and interactive
            user experiences using JavaScript and React.
            """,

            "projects": """
            Build frontend websites and web applications
            using HTML, CSS, JavaScript and React.
            """
        }
    }

    # =====================================================
    # RESULTS
    # =====================================================

    results = []

    for job_type, job in jobs.items():

        # ---------------------------------------------
        # Skills similarity
        # ---------------------------------------------

        resume_skill_embedding = matcher.create_embedding(
            resume["skills"]
        )

        job_skill_embedding = matcher.create_embedding(
            job["skills"]
        )

        skills_score = scorer.calculate_similarity(
            resume_skill_embedding,
            job_skill_embedding
        )

        # ---------------------------------------------
        # Experience similarity
        # ---------------------------------------------

        resume_experience_embedding = matcher.create_embedding(
            resume["experience"]
        )

        job_experience_embedding = matcher.create_embedding(
            job["experience"]
        )

        experience_score = scorer.calculate_similarity(
            resume_experience_embedding,
            job_experience_embedding
        )

        # ---------------------------------------------
        # Project similarity
        # ---------------------------------------------

        resume_project_embedding = matcher.create_embedding(
            resume["projects"]
        )

        job_project_embedding = matcher.create_embedding(
            job["projects"]
        )

        projects_score = scorer.calculate_similarity(
            resume_project_embedding,
            job_project_embedding
        )

        # ---------------------------------------------
        # Final weighted score
        # ---------------------------------------------

        final_score = scorer.calculate_weighted_score(
            skills_score,
            experience_score,
            projects_score
        )

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

        classification = scorer.classify_match(
            final_percentage
        )

        # ---------------------------------------------
        # Store result
        # ---------------------------------------------

        results.append({
            "Job Type": job_type,
            "Skills Score": skills_percentage,
            "Experience Score": experience_percentage,
            "Projects Score": projects_percentage,
            "Final Match Score": final_percentage,
            "Classification": classification
        })

    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    report = pd.DataFrame(results)

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    print("\n")
    print("=" * 75)
    print("              ZECpath AI JOB TYPE VALIDATION")
    print("=" * 75)

    print(report.to_string(index=False))

    print("=" * 75)

    # =====================================================
    # SAVE REPORT
    # =====================================================

    output_folder = Path("outputs")
    output_folder.mkdir(exist_ok=True)

    output_file = output_folder / "matching_report.csv"

    report.to_csv(
        output_file,
        index=False
    )

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
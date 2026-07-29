"""
Day 12 - Real Resume <-> Job Description Semantic Matching

Connects:
Day 5  -> ResumeTextExtractor
Day 6  -> JobDescriptionParser
Day 9  -> SkillExtractor
Day 10 -> ExperienceParser
Day 12 -> SemanticMatcher + SimilarityScorer
"""

from parsers.resume_text_extractor import ResumeTextExtractor
from parsers.jd_parser import JobDescriptionParser
from parsers.skill_extractor import SkillExtractor
from parsers.experience_parser import ExperienceParser

from semantic_matching.semantic_matcher import SemanticMatcher
from semantic_matching.similarity_scorer import SimilarityScorer


class ResumeJobMatcher:

    def __init__(self):

        print("Loading ZECpath AI Semantic Matching Engine...")

        self.text_extractor = ResumeTextExtractor()
        self.jd_parser = JobDescriptionParser()
        self.skill_extractor = SkillExtractor()
        self.experience_parser = ExperienceParser()

        self.semantic_matcher = SemanticMatcher()
        self.scorer = SimilarityScorer()

        print("Semantic Matching Engine Ready.")

    # ---------------------------------------------------------
    # RESUME PROCESSING
    # ---------------------------------------------------------

    def extract_resume_data(self, resume_path):

        print("\nExtracting resume...")

        result = self.text_extractor.extract_and_process(
            resume_path
        )

        resume_text = result["cleaned_text"]

        # Day 9 skill extraction
        skills_data = self.skill_extractor.extract(
            resume_text
        )

        skills = [
            item["skill"]
            for item in skills_data
        ]

        # Day 10 experience extraction
        experiences = self.experience_parser.parse_experience(
            resume_text
        )

        # Create semantic experience representation
        experience_text = ""

        for experience in experiences:

            experience_text += (
                f"{experience['job_title']} "
                f"at {experience['company']}. "
                f"Experience duration: "
                f"{experience['duration_months']} months. "
            )

        # Fallback if experience parser doesn't find
        # structured jobs.
        if not experience_text:
            experience_text = resume_text

        return {
            "raw_text": resume_text,
            "skills": skills,
            "skills_data": skills_data,
            "experiences": experiences,
            "experience_text": experience_text,
            "projects_text": resume_text
        }

    # ---------------------------------------------------------
    # JD PROCESSING
    # ---------------------------------------------------------

    def parse_job_description(self, jd_text):

        print("\nParsing job description...")

        jd_data = self.jd_parser.parse(
            jd_text
        )

        return jd_data

    # ---------------------------------------------------------
    # SEMANTIC MATCHING
    # ---------------------------------------------------------

    def calculate_similarity(
        self,
        resume_data,
        jd_data
    ):

        print("\nCalculating semantic similarity...")

        # =====================================================
        # SKILLS
        # =====================================================

        resume_skills_text = ", ".join(
            resume_data["skills"]
        )

        jd_skills_text = ", ".join(
            jd_data["required_skills"]
        )

        # If the parser finds no skills, use the complete JD
        # as a fallback representation.
        if not jd_skills_text:
            jd_skills_text = jd_data["cleaned_text"]

        resume_skill_embedding = (
            self.semantic_matcher.create_embedding(
                resume_skills_text
            )
        )

        jd_skill_embedding = (
            self.semantic_matcher.create_embedding(
                jd_skills_text
            )
        )

        skills_score = self.scorer.calculate_similarity(
            resume_skill_embedding,
            jd_skill_embedding
        )

        # =====================================================
        # EXPERIENCE
        # =====================================================

        resume_experience_embedding = (
            self.semantic_matcher.create_embedding(
                resume_data["experience_text"]
            )
        )

        # Use complete JD because it contains responsibilities,
        # requirements and role context.
        jd_experience_embedding = (
            self.semantic_matcher.create_embedding(
                jd_data["cleaned_text"]
            )
        )

        experience_score = self.scorer.calculate_similarity(
            resume_experience_embedding,
            jd_experience_embedding
        )

        # =====================================================
        # PROJECT / OVERALL SEMANTIC SIMILARITY
        # =====================================================

        resume_project_embedding = (
            self.semantic_matcher.create_embedding(
                resume_data["projects_text"]
            )
        )

        jd_project_embedding = (
            self.semantic_matcher.create_embedding(
                jd_data["cleaned_text"]
            )
        )

        projects_score = self.scorer.calculate_similarity(
            resume_project_embedding,
            jd_project_embedding
        )

        # =====================================================
        # FINAL WEIGHTED SCORE
        # =====================================================

        final_score = self.scorer.calculate_weighted_score(
            skills_score,
            experience_score,
            projects_score
        )

        skills_percentage = self.scorer.to_percentage(
            skills_score
        )

        experience_percentage = self.scorer.to_percentage(
            experience_score
        )

        projects_percentage = self.scorer.to_percentage(
            projects_score
        )

        final_percentage = self.scorer.to_percentage(
            final_score
        )

        classification = self.scorer.classify_match(
            final_percentage
        )

        return {
            "skills_score": skills_percentage,
            "experience_score": experience_percentage,
            "projects_score": projects_percentage,
            "final_score": final_percentage,
            "classification": classification
        }

    # ---------------------------------------------------------
    # COMPLETE MATCHING PIPELINE
    # ---------------------------------------------------------

    def match(
        self,
        resume_path,
        jd_text
    ):

        resume_data = self.extract_resume_data(
            resume_path
        )

        jd_data = self.parse_job_description(
            jd_text
        )

        scores = self.calculate_similarity(
            resume_data,
            jd_data
        )

        return {
            "resume": resume_data,
            "job_description": jd_data,
            "scores": scores
        }
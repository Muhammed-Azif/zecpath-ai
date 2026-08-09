"""
Day 12 - Real Resume <-> Job Description Semantic Matching

Day 18 performance enhancements:
- Cache repeated embeddings
- Avoid duplicate JD embedding generation
- Avoid duplicate resume embedding generation
- Measure semantic matching time
- Preserve existing scoring behavior and API
"""

import logging
import time
from functools import lru_cache

from parsers.resume_text_extractor import ResumeTextExtractor
from parsers.jd_parser import JobDescriptionParser
from parsers.skill_extractor import SkillExtractor
from parsers.experience_parser import ExperienceParser

from semantic_matching.semantic_matcher import SemanticMatcher
from semantic_matching.similarity_scorer import SimilarityScorer


logger = logging.getLogger(__name__)


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
    # EMBEDDING CACHE
    # ---------------------------------------------------------

    @lru_cache(maxsize=128)
    def _create_cached_embedding(self, text):
        """
        Create an embedding and cache repeated requests.

        This prevents the same text from being embedded multiple
        times during a single matching operation.
        """

        if not text:
            return None

        return self.semantic_matcher.create_embedding(text)

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
        experience_parts = []

        for experience in experiences:

            experience_parts.append(
                f"{experience['job_title']} "
                f"at {experience['company']}. "
                f"Experience duration: "
                f"{experience['duration_months']} months."
            )

        experience_text = " ".join(experience_parts)

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

        start_time = time.perf_counter()

        # =====================================================
        # SKILLS
        # =====================================================

        resume_skills_text = ", ".join(
            resume_data["skills"]
        )

        jd_skills_text = ", ".join(
            jd_data["required_skills"]
        )

        # If parser finds no skills, use complete JD.
        if not jd_skills_text:
            jd_skills_text = jd_data["cleaned_text"]

        resume_skill_embedding = (
            self._create_cached_embedding(
                resume_skills_text
            )
        )

        jd_skill_embedding = (
            self._create_cached_embedding(
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
            self._create_cached_embedding(
                resume_data["experience_text"]
            )
        )

        # Create this embedding only once.
        jd_full_embedding = (
            self._create_cached_embedding(
                jd_data["cleaned_text"]
            )
        )

        experience_score = self.scorer.calculate_similarity(
            resume_experience_embedding,
            jd_full_embedding
        )

        # =====================================================
        # PROJECT / OVERALL SEMANTIC SIMILARITY
        # =====================================================

        resume_project_embedding = (
            self._create_cached_embedding(
                resume_data["projects_text"]
            )
        )

        # Reuse the already-created JD embedding.
        projects_score = self.scorer.calculate_similarity(
            resume_project_embedding,
            jd_full_embedding
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

        elapsed = time.perf_counter() - start_time

        logger.info(
            "Performance | semantic_similarity | %.4f seconds",
            elapsed
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

        start_time = time.perf_counter()

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

        elapsed = time.perf_counter() - start_time

        logger.info(
            "Performance | complete_resume_job_matching | %.4f seconds",
            elapsed
        )

        return {
            "resume": resume_data,
            "job_description": jd_data,
            "scores": scores
        }
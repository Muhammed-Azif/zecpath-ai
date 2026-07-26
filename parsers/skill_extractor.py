"""
Day 9 - Skill Extraction Engine

Extracts technical, business and creative skills
from resume text using dictionary matching and NLP.
"""

import re
import spacy
from utils.skill_dictionary import get_all_skills
from utils.skill_normalizer import SkillNormalizer
from utils.confidence_scorer import SkillConfidenceScorer

class SkillExtractor:

    def __init__(self):
        self.normalizer = SkillNormalizer()
        self.master_skills = get_all_skills()
        self.nlp = spacy.load("en_core_web_sm")
        self.confidence_scorer = SkillConfidenceScorer()

    def extract_dictionary_skills(self, text):
        """
        Extract skills using the master skill dictionary.
        """

        if not text:
            return []

        found_skills = []

        text_lower = text.lower()

        for skill in self.master_skills:

            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text_lower):
                found_skills.append(skill)

        return found_skills

    def extract_synonym_skills(self, text):
        """
        Detect known skill synonyms.
        """

        if not text:
            return []

        found_skills = []

        text_lower = text.lower()

        for synonym, canonical in self.normalizer.synonyms.items():

            pattern = r"\b" + re.escape(synonym.lower()) + r"\b"

            if re.search(pattern, text_lower):
                found_skills.append(canonical)

        return found_skills

    def extract_stack_skills(self, text):
        """
        Detect skill stacks such as MERN and MEAN
        and expand them into their component skills.
        """

        if not text:
            return []

        found_skills = []

        for stack_name, skills in self.normalizer.skill_stacks.items():

            pattern = r"\b" + re.escape(stack_name.lower()) + r"\b"

            if re.search(pattern, text.lower()):
                found_skills.extend(skills)

        return found_skills
    def extract(self, text):
        """
        Main Day 9 skill extraction pipeline.

        Combines:
        - Exact dictionary matching
        - Synonym matching
        - Skill-stack expansion
        - NLP candidate detection
        - Normalization
        - Deduplication
        - Confidence scoring
        """

        if not text:
            return []

        # --------------------------------------------------
        # 1. Extract using different detection methods
        # --------------------------------------------------

        dictionary_skills = self.extract_dictionary_skills(text)

        synonym_skills = self.extract_synonym_skills(text)

        stack_skills = self.extract_stack_skills(text)

        nlp_candidates = self.extract_nlp_candidates(text)

        # --------------------------------------------------
        # 2. Store detection evidence
        # --------------------------------------------------

        evidence = {}

        def add_evidence(skill, method):
            canonical = self.normalizer.normalize(skill)

            if canonical:
                evidence.setdefault(canonical, set())
                evidence[canonical].add(method)

        for skill in dictionary_skills:
            add_evidence(skill, "exact_match")

        for skill in synonym_skills:
            add_evidence(skill, "synonym_match")

        for skill in stack_skills:
            add_evidence(skill, "skill_stack")

        for candidate in nlp_candidates:
            add_evidence(candidate, "nlp_match")

        # --------------------------------------------------
        # 3. Create structured output
        # --------------------------------------------------

        results = []

        for skill, methods in evidence.items():

            confidence_data = self.confidence_scorer.score_skill(
                skill,
                list(methods)
            )

            results.append({
                "skill": skill,
                "category": self.normalizer.get_category(skill),
                "confidence": confidence_data["confidence"],
                "detection_methods": sorted(methods)
            })

        # --------------------------------------------------
        # 4. Sort by confidence
        # --------------------------------------------------

        results.sort(
            key=lambda item: item["confidence"],
            reverse=True
        )

        return results

    def extract_nlp_candidates(self, text):
        """
        Use spaCy NLP to identify candidate skill phrases.
        """

        if not text:
            return []

        doc = self.nlp(text)

        candidates = []

        # Named entities
        for ent in doc.ents:
            candidates.append(ent.text)

        # Noun chunks can contain skill phrases
        for chunk in doc.noun_chunks:
            candidates.append(chunk.text)

        return candidates
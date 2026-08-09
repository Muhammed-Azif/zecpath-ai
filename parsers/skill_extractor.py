"""
Day 9 - Skill Extraction Engine

Day 18 enhancements:
- Pre-compile skill and synonym regex patterns
- Avoid repeated lower() calls
- Disable unnecessary spaCy pipeline components
- Cache repeated NLP processing
- Preserve existing structured output
- Preserve existing skill detection behavior
"""

import logging
import re
from functools import lru_cache

import spacy

from utils.skill_dictionary import get_all_skills
from utils.skill_normalizer import SkillNormalizer
from utils.confidence_scorer import SkillConfidenceScorer


logger = logging.getLogger(__name__)


class SkillExtractor:

    def __init__(self):

        self.normalizer = SkillNormalizer()

        self.master_skills = get_all_skills()

        # --------------------------------------------------
        # Pre-compile exact skill patterns once.
        # --------------------------------------------------

        self.skill_patterns = [
            (
                skill,
                re.compile(
                    r"\b" + re.escape(skill.lower()) + r"\b"
                )
            )
            for skill in self.master_skills
        ]

        # --------------------------------------------------
        # Pre-compile synonym patterns once.
        # --------------------------------------------------

        self.synonym_patterns = [
            (
                synonym,
                canonical,
                re.compile(
                    r"\b" + re.escape(synonym.lower()) + r"\b"
                )
            )
            for synonym, canonical
            in self.normalizer.synonyms.items()
        ]

        # --------------------------------------------------
        # Pre-compile skill-stack patterns once.
        # --------------------------------------------------

        self.stack_patterns = [
            (
                stack_name,
                skills,
                re.compile(
                    r"\b" + re.escape(stack_name.lower()) + r"\b"
                )
            )
            for stack_name, skills
            in self.normalizer.skill_stacks.items()
        ]

        # --------------------------------------------------
        # Load spaCy with only the components needed for
        # entity and noun-chunk detection.
        # --------------------------------------------------

        self.nlp = spacy.load(
            "en_core_web_sm",
            disable=[
                "textcat",
                "lemmatizer"
            ]
        )

        self.confidence_scorer = SkillConfidenceScorer()

    # ------------------------------------------------------
    # DICTIONARY MATCHING
    # ------------------------------------------------------

    def extract_dictionary_skills(self, text):
        """
        Extract skills using the master skill dictionary.
        """

        if not text:
            return []

        text_lower = text.lower()

        found_skills = []

        for skill, pattern in self.skill_patterns:

            if pattern.search(text_lower):
                found_skills.append(skill)

        return found_skills

    # ------------------------------------------------------
    # SYNONYM MATCHING
    # ------------------------------------------------------

    def extract_synonym_skills(self, text):
        """
        Detect known skill synonyms.
        """

        if not text:
            return []

        text_lower = text.lower()

        found_skills = []

        for synonym, canonical, pattern in self.synonym_patterns:

            if pattern.search(text_lower):
                found_skills.append(canonical)

        return found_skills

    # ------------------------------------------------------
    # SKILL STACK MATCHING
    # ------------------------------------------------------

    def extract_stack_skills(self, text):
        """
        Detect skill stacks such as MERN and MEAN
        and expand them into their component skills.
        """

        if not text:
            return []

        text_lower = text.lower()

        found_skills = []

        for stack_name, skills, pattern in self.stack_patterns:

            if pattern.search(text_lower):
                found_skills.extend(skills)

        return found_skills

    # ------------------------------------------------------
    # MAIN EXTRACTION
    # ------------------------------------------------------

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
                evidence.setdefault(
                    canonical,
                    set()
                )

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

            confidence_data = (
                self.confidence_scorer.score_skill(
                    skill,
                    list(methods)
                )
            )

            results.append({
                "skill": skill,
                "category": self.normalizer.get_category(
                    skill
                ),
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

    # ------------------------------------------------------
    # NLP CANDIDATE DETECTION
    # ------------------------------------------------------

    @lru_cache(maxsize=64)
    def _extract_nlp_candidates_cached(self, text):
        """
        Cached NLP processing for repeated resume text.

        Avoids running spaCy again when exactly the same text
        is processed repeatedly.
        """

        doc = self.nlp(text)

        candidates = []

        # Named entities
        for ent in doc.ents:
            candidates.append(ent.text)

        # Noun chunks
        for chunk in doc.noun_chunks:
            candidates.append(chunk.text)

        return tuple(candidates)

    def extract_nlp_candidates(self, text):
        """
        Use spaCy NLP to identify candidate skill phrases.
        """

        if not text:
            return []

        return list(
            self._extract_nlp_candidates_cached(text)
        )
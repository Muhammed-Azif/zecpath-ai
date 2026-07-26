"""
Day 9 - Skill Normalizer

Normalizes skill names, handles synonyms, expands skill stacks,
and removes duplicate skills.
"""

from utils.skill_dictionary import (
    SKILL_SYNONYMS,
    SKILL_STACKS,
    get_all_skills,
    get_skill_category
)


class SkillNormalizer:

    def __init__(self):
        self.synonyms = SKILL_SYNONYMS
        self.skill_stacks = SKILL_STACKS
        self.master_skills = get_all_skills()

        # Case-insensitive lookup
        self.master_lookup = {
            skill.lower(): skill
            for skill in self.master_skills
        }

    def normalize(self, skill):
        """
        Convert a skill name into its canonical form.
        """

        if not skill:
            return None

        cleaned = skill.strip()

        if not cleaned:
            return None

        # Exact canonical skill
        if cleaned.lower() in self.master_lookup:
            return self.master_lookup[cleaned.lower()]

        # Synonym
        synonym = self.synonyms.get(cleaned.lower())

        if synonym:
            return synonym

        return None

    def expand_stack(self, skill):
        """
        Expand skill stacks such as MERN and MEAN.
        """

        cleaned = skill.strip().upper()

        for stack_name, skills in self.skill_stacks.items():

            if cleaned == stack_name.upper():
                return skills

        return []

    def normalize_and_expand(self, skills):
        """
        Normalize skills, expand stacks and remove duplicates.
        """

        normalized = []

        for skill in skills:

            # Check if it is a skill stack
            expanded = self.expand_stack(skill)

            if expanded:
                normalized.extend(expanded)
                continue

            # Normal skill/synonym
            canonical = self.normalize(skill)

            if canonical:
                normalized.append(canonical)

        # Remove duplicates while preserving order
        unique_skills = []
        seen = set()

        for skill in normalized:

            key = skill.lower()

            if key not in seen:
                seen.add(key)
                unique_skills.append(skill)

        return unique_skills

    def get_category(self, skill):
        """
        Return the category of a normalized skill.
        """

        return get_skill_category(skill)
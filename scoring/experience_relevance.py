"""
Day 10 - Experience Relevance Engine
"""

import re

class ExperienceRelevance:

    def __init__(self):
        pass

    def extract_keywords(self, text):
        """
        Extracts important keywords from text.
        """

        text = text.lower()

        words = re.findall(r"\b[a-zA-Z]+\b", text)

        stop_words = {
            "the", "and", "for", "with", "to",
            "of", "in", "on", "a", "an", "is",
            "are", "will", "be", "have"
        }

        keywords = []

        for word in words:

            if word not in stop_words:

                keywords.append(word)

        return set(keywords)

    def calculate_relevance(
        self,
        experiences,
        job_title,
        job_description
    ):
        """
        Calculates experience relevance score.
        """

        job_keywords = self.extract_keywords(
            job_title + " " + job_description
        )

        candidate_keywords = set()

        for job in experiences:

            candidate_keywords.update(
                self.extract_keywords(job["job_title"])
            )

            candidate_keywords.update(
                self.extract_keywords(job["company"])
            )

        matched = candidate_keywords & job_keywords

        missing = job_keywords - candidate_keywords

        if len(job_keywords) == 0:

            score = 0

        else:

            score = round(
                len(matched) /
                len(job_keywords)
                * 100,
                2
            )

        return {
            "experience_relevance_score": score,
            "matched_keywords": sorted(list(matched)),
            "missing_keywords": sorted(list(missing))
        }
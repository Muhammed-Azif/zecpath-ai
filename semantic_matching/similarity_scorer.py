from sklearn.metrics.pairwise import cosine_similarity


class SimilarityScorer:
    """
    Calculates semantic similarity and weighted
    resume-job matching scores.
    """

    @staticmethod
    def calculate_similarity(embedding1, embedding2):
        """
        Calculate cosine similarity between embeddings.
        """

        score = cosine_similarity(
            [embedding1],
            [embedding2]
        )[0][0]

        return float(score)

    @staticmethod
    def calculate_weighted_score(
        skills_score,
        experience_score,
        projects_score
    ):
        """
        Calculate the final weighted semantic score.

        Skills      = 40%
        Experience  = 30%
        Projects    = 30%
        """

        final_score = (
            skills_score * 0.40
            + experience_score * 0.30
            + projects_score * 0.30
        )

        return final_score

    @staticmethod
    def to_percentage(score):
        """
        Convert similarity score into percentage.
        """

        return round(score * 100, 2)

    @staticmethod
    def classify_match(percentage):
        """
        Classify candidate-job match.
        """

        if percentage >= 75:
            return "Excellent Match"

        elif percentage >= 60:
            return "Good Match"

        elif percentage >= 45:
            return "Moderate Match"

        else:
            return "Low Match"
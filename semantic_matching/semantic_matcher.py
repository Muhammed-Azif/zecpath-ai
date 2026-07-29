from sentence_transformers import SentenceTransformer


class SemanticMatcher:
    """
    Converts resume and job description sections
    into semantic embeddings.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_embedding(self, text):
        """
        Convert text into a semantic embedding.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        return self.model.encode(text)

    def compare_sections(self, resume_section, job_section):
        """
        Generate embeddings for two sections.
        """

        resume_embedding = self.create_embedding(resume_section)
        job_embedding = self.create_embedding(job_section)

        return resume_embedding, job_embedding
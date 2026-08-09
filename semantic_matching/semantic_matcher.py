"""
Day 12 - Semantic Matching Engine

Day 18 performance enhancements:
- Reuse a single SentenceTransformer model across instances
- Reduce unnecessary model-loading overhead
- Disable progress output during inference
- Preserve existing embedding behavior
- Add lightweight performance monitoring
"""

import logging
import time

from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


class SemanticMatcher:
    """
    Converts resume and job description sections
    into semantic embeddings.
    """

    # Shared model instance.
    # This prevents loading the same model multiple times
    # when multiple SemanticMatcher objects are created.
    _model = None

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self):

        if SemanticMatcher._model is None:

            logger.info(
                "Loading semantic model: %s",
                self.MODEL_NAME
            )

            start_time = time.perf_counter()

            SemanticMatcher._model = SentenceTransformer(
                self.MODEL_NAME
            )

            elapsed = time.perf_counter() - start_time

            logger.info(
                "Semantic model loaded in %.4f seconds",
                elapsed
            )

        self.model = SemanticMatcher._model

    def create_embedding(self, text):
        """
        Convert text into a semantic embedding.

        Existing behavior is preserved:
        - Empty text raises ValueError.
        - Same SentenceTransformer model is used.
        - Embeddings are returned as numpy arrays.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        start_time = time.perf_counter()

        embedding = self.model.encode(
            text,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=False
        )

        elapsed = time.perf_counter() - start_time

        logger.debug(
            "Embedding generated in %.4f seconds",
            elapsed
        )

        return embedding

    def compare_sections(self, resume_section, job_section):
        """
        Generate embeddings for two sections.
        """

        resume_embedding = self.create_embedding(
            resume_section
        )

        job_embedding = self.create_embedding(
            job_section
        )

        return resume_embedding, job_embedding
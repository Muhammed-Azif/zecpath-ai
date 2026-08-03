from screening_ai.bias_detector import BiasDetector
from screening_ai.resume_normalizer import ResumeNormalizer
from screening_ai.score_normalizer import ScoreNormalizer


class FairnessEngine:

    def __init__(self):

        self.bias = BiasDetector()
        self.resume = ResumeNormalizer()
        self.score = ScoreNormalizer()

    def process(self, resume, ats_score):

        normalized_resume = self.resume.normalize(resume)

        masked_text = self.bias.mask_personal_information(
            normalized_resume.get("text", "")
        )

        normalized_resume["text"] = masked_text

        final_score = self.score.normalize(ats_score)

        return {

            "resume": normalized_resume,

            "normalized_score": final_score,

            "bias_removed": True

        }
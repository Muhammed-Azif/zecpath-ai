from ats_engine.ats_scorer import ATSScorer
from parsers.resume_text_extractor import extract_and_process

class ATSService:
    def __init__(self, role="Default"):
        self.scorer = ATSScorer(role)

    def calculate_score(
        self,
        skills_score,
        experience_score,
        education_score,
        semantic_score,
    ):
        return self.scorer.calculate_score(
            skills_score=skills_score,
            experience_score=experience_score,
            education_score=education_score,
            semantic_score=semantic_score,
        )

    def shortlist(self, overall_score, threshold=70):
        return {
            "status": "Selected" if overall_score >= threshold else "Rejected",
            "overall_score": overall_score,
            "threshold": threshold,
        }

    def parse_resume(self, file_path):
        result = extract_and_process(
            file_path=file_path,
            output_dir="outputs/extracted"
        )

        return result
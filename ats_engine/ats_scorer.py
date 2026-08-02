from ats_engine.weight_config import ROLE_WEIGHTS, DEFAULT_WEIGHTS


class ATSScorer:

    def __init__(self, role="Default"):

        self.weights = ROLE_WEIGHTS.get(role, DEFAULT_WEIGHTS)

    def calculate_score(
            self,
            skills_score,
            experience_score,
            education_score,
            semantic_score):

        skills_score = skills_score or 0
        experience_score = experience_score or 0
        education_score = education_score or 0
        semantic_score = semantic_score or 0

        skills = skills_score * self.weights["skills"]
        experience = experience_score * self.weights["experience"]
        education = education_score * self.weights["education"]
        semantic = semantic_score * self.weights["semantic"]

        final = skills + experience + education + semantic

        return {
            "skills": round(skills_score, 2),
            "experience": round(experience_score, 2),
            "education": round(education_score, 2),
            "semantic": round(semantic_score, 2),

            "final_score": round(final, 2),

            "classification": self.classify(final),

            "breakdown": {

                "skills": round(skills, 2),

                "experience": round(experience, 2),

                "education": round(education, 2),

                "semantic": round(semantic, 2)

            }
        }

    def classify(self, score):

        if score >= 90:
            return "Outstanding"

        elif score >= 80:
            return "Excellent"

        elif score >= 70:
            return "Good"

        elif score >= 60:
            return "Fair"

        return "Weak"
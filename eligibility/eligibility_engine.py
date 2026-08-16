"""
Day 21 - Eligibility Decision Engine

Determines whether a candidate is:
    - Eligible
    - Review
    - Rejected

based on ATS score and recruiter-defined job rules.
"""

from eligibility.rule_config import get_rules


class EligibilityDecisionEngine:

    def __init__(self, role="Default"):
        self.role = role
        self.rules = get_rules(role)

    def evaluate(self, candidate):
        """
        Evaluate a candidate against configured eligibility rules.
        """

        candidate_id = candidate.get("candidate_id")
        job_id = candidate.get("job_id")

        ats_score = candidate.get("ats_score", 0)
        candidate_skills = candidate.get("skills", [])
        experience_years = candidate.get("experience_years", 0)
        location = candidate.get("location", "")
        available = candidate.get("available", False)

        candidate_skills_normalized = {
            skill.strip().lower()
            for skill in candidate_skills
        }

        mandatory_skills = self.rules.get("mandatory_skills", [])

        matched_skills = [
            skill
            for skill in mandatory_skills
            if skill.lower() in candidate_skills_normalized
        ]

        missing_skills = [
            skill
            for skill in mandatory_skills
            if skill.lower() not in candidate_skills_normalized
        ]

        reasons = []
        warnings = []

        decision = "Eligible"

        # ---------------------------------------------------------
        # 1. Mandatory skill check
        # ---------------------------------------------------------

        if missing_skills:
            decision = "Rejected"

            reasons.append(
                "Missing mandatory skills: "
                + ", ".join(missing_skills)
            )

        else:
            reasons.append(
                "All mandatory skills are present"
            )

        # ---------------------------------------------------------
        # 2. Experience check
        # ---------------------------------------------------------

        min_experience = self.rules.get(
            "minimum_experience", 0
        )

        max_experience = self.rules.get(
            "maximum_experience", 50
        )

        if (
            experience_years < min_experience
            or experience_years > max_experience
        ):
            if decision != "Rejected":
                decision = "Review"

            reasons.append(
                f"Experience ({experience_years} years) "
                f"is outside the preferred range "
                f"({min_experience}-{max_experience} years)"
            )

        else:
            reasons.append(
                "Experience is within the required range"
            )

        # ---------------------------------------------------------
        # 3. Location check
        # ---------------------------------------------------------

        allowed_locations = self.rules.get(
            "allowed_locations", []
        )

        if allowed_locations:

            location_match = any(
                location.lower() == allowed.lower()
                for allowed in allowed_locations
            )

            if not location_match:

                if decision != "Rejected":
                    decision = "Review"

                reasons.append(
                    f"Location '{location}' is outside "
                    "the configured locations"
                )

                warnings.append(
                    "Location requires recruiter review"
                )

            else:
                reasons.append(
                    "Location satisfies job requirements"
                )

        # ---------------------------------------------------------
        # 4. Availability check
        # ---------------------------------------------------------

        availability_required = self.rules.get(
            "availability_required",
            False
        )

        if availability_required and not available:

            if decision != "Rejected":
                decision = "Review"

            reasons.append(
                "Candidate availability does not "
                "satisfy the job requirement"
            )

            warnings.append(
                "Availability requires recruiter review"
            )

        elif availability_required:

            reasons.append(
                "Candidate satisfies availability requirement"
            )

        # ---------------------------------------------------------
        # 5. ATS score check
        # ---------------------------------------------------------

        minimum_ats_score = self.rules.get(
            "minimum_ats_score",
            70
        )

        review_score = self.rules.get(
            "review_score",
            50
        )

        if ats_score < review_score:

            decision = "Rejected"

            reasons.append(
                f"ATS score ({ats_score}) is below "
                f"review threshold ({review_score})"
            )

        elif ats_score < minimum_ats_score:

            if decision != "Rejected":
                decision = "Review"

            reasons.append(
                f"ATS score ({ats_score}) is below "
                f"eligibility threshold ({minimum_ats_score})"
            )

        else:

            reasons.append(
                f"ATS score ({ats_score}) meets "
                f"minimum requirement ({minimum_ats_score})"
            )

        # ---------------------------------------------------------
        # Final result
        # ---------------------------------------------------------
        if decision != "Review":
            warnings = []
        return {
            "candidate_id": candidate_id,
            "job_id": job_id,
            "role": self.role,

            "decision": decision,

            "ats_score": ats_score,

            "matched_mandatory_skills": matched_skills,
            "missing_mandatory_skills": missing_skills,

            "experience_years": experience_years,
            "location": location,
            "available": available,

            "reasons": reasons,
            "warnings": warnings
        }
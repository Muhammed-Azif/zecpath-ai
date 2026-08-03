class ResumeNormalizer:

    def normalize(self, resume):

        normalized = resume.copy()

        # Remove duplicate spaces
        for key, value in normalized.items():

            if isinstance(value, str):
                normalized[key] = " ".join(value.split())

        return normalized
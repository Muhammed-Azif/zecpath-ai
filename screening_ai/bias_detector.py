import re


class BiasDetector:

    def mask_personal_information(self, text):

        patterns = {

            "email":
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            "phone":
            r"\+?\d[\d\s\-]{8,}",

            "gender":
            r"\b(male|female|man|woman)\b",

            "marital":
            r"\b(single|married|divorced)\b",

            "age":
            r"\b\d{2}\s*years?\s*old\b"

        }

        masked = text

        for pattern in patterns.values():
            masked = re.sub(pattern, "[MASKED]", masked,
                            flags=re.IGNORECASE)

        return masked
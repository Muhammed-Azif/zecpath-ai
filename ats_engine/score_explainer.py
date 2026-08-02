class ScoreExplainer:

    def explain(self, result):

        print()

        print("=" * 55)
        print("             ZECPATH AI ATS SCORE")
        print("=" * 55)

        print(f"Skill Match        : {result['skills']}%")
        print(f"Experience         : {result['experience']}%")
        print(f"Education          : {result['education']}%")
        print(f"Semantic Match     : {result['semantic']}%")

        print("-" * 55)

        print(f"Final ATS Score    : {result['final_score']}%")
        print(f"Classification     : {result['classification']}")

        print("-" * 55)

        print("Score Breakdown")

        print(
            f"Skills Contribution      : {result['breakdown']['skills']}")
        print(
            f"Experience Contribution  : {result['breakdown']['experience']}")
        print(
            f"Education Contribution   : {result['breakdown']['education']}")
        print(
            f"Semantic Contribution    : {result['breakdown']['semantic']}")

        print("=" * 55)
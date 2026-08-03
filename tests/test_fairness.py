from screening_ai.fairness_engine import FairnessEngine


resume = {

    "name":"John",

    "text":"""
Male
Age 24 years old

Phone +91 9876543210

Email john@gmail.com

Python Developer
"""

}

engine = FairnessEngine()

result = engine.process(resume,88.7)

print()

print("="*50)
print("ZECPATH FAIRNESS ENGINE")
print("="*50)

print(result["resume"]["text"])

print()

print("Normalized Score:",result["normalized_score"])

print("Bias Removed:",result["bias_removed"])
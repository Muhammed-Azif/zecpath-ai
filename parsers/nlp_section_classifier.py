from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

SECTION_LABELS = [
    "Summary",
    "Skills",
    "Work Experience",
    "Education",
    "Certifications",
    "Projects",
    "Achievements",
    "Languages",
    "Contact"
]

label_embeddings = model.encode(SECTION_LABELS, convert_to_tensor=True)

def predict_section(heading):
    embedding = model.encode(heading, convert_to_tensor=True)
    scores = util.cos_sim(embedding, label_embeddings)

    best_score = scores.max().item()
    best_idx = scores.argmax().item()

    if best_score > 0.55:  # confidence threshold
        return SECTION_LABELS[best_idx]

    return None
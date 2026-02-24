# embeddings.py
# Purpose: Converts user answers and reference explanation into semantic embeddings,
# computes cosine similarity for cross-answer consistency and reference alignment,
# and returns the combined semantic stability score.
# Primary Owner: Sparsho Sengupta

import numpy as np
import google.genai as genai
from typing import List

# CONFIGURATION

genai.configure(api_key="GEMINI_API_KEY")

# EMBEDDING GENERATION


def generate_embedding(text: str, model: str = "models/embedding-001") -> List[float]:

    response = genai.embed_content(model=model, content=text)
    return response["embedding"]


# COSINE SIMILARITY


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:

    v1 = np.array(vec1)
    v2 = np.array(vec2)

    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0

    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return float(similarity)


# WORD COUNT VALIDATION


def is_valid_length(text: str, min_words: int = 25) -> bool:

    word_count = len(text.strip().split())
    return word_count >= min_words


# CROSS ANSWER SIMILARITY (CAS)


def compute_cross_similarity(answers: List[str]) -> float:

    if len(answers) < 2:
        return 0.0

    embeddings = [generate_embedding(ans) for ans in answers]

    similarities = []

    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            similarities.append(sim)

    if not similarities:
        return 0.0

    return float(np.mean(similarities))


# REFERENCE ALIGNMENT (RAS)


def compute_reference_similarity(answers: List[str], reference_text: str) -> float:

    reference_embedding = generate_embedding(reference_text)

    similarities = []

    for ans in answers:
        ans_embedding = generate_embedding(ans)
        sim = cosine_similarity(ans_embedding, reference_embedding)
        similarities.append(sim)

    if not similarities:
        return 0.0

    return float(np.mean(similarities))


# FINAL SEMANTIC SCORE


def compute_semantic_score(
    answers: List[str], reference_text: str, min_words: int = 25
) -> float:

    for ans in answers:
        if not is_valid_length(ans, min_words):
            raise ValueError(
                "One or more answers do not meet minimum word requirement."
            )

    cross_similarity = compute_cross_similarity(answers)
    reference_similarity = compute_reference_similarity(answers, reference_text)

    semantic_score = (0.5 * cross_similarity) + (0.5 * reference_similarity)

    return round(semantic_score, 4)

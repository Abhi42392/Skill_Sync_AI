from functools import lru_cache
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


@lru_cache(maxsize=1)
def _get_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_text(text: str) -> List[float]:
    if not text or not text.strip():
        return [0.0] * settings.EMBEDDING_DIM

    model = _get_model()
    vector = model.encode(
        text,
        normalize_embeddings=True
    )

    return vector.tolist()


def embed_texts(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []

    model = _get_model()

    vectors = model.encode(
        texts,
        normalize_embeddings=True
    )

    return [v.tolist() for v in np.atleast_2d(vectors)]


def cosine_similarity(
    vec_a: List[float],
    vec_b: List[float]
) -> float:

    a = np.array(vec_a)
    b = np.array(vec_b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)
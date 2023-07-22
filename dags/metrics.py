import numpy as np
from vectorizer import Vector


def cosine_similarity(vec1: Vector, vec2: Vector) -> float:
    vec1 = vec1
    vec2 = vec2
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

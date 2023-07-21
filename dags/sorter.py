from typing import List

from vectorizer import Vector
from interpretation import InterpretableVector
from metrics import cosine_similarity


class CVSorter:
    def __init__(self, prompt_vector: Vector, cv_vectors: list[Vector]):
        self.prompt = prompt_vector
        self.cvs = cv_vectors

    def sort_cvs(self, top_n: int or None = None) -> list[InterpretableVector]:
        results = []
        if top_n is None:
            top_n = len(self.cvs)

        for vec in self.cvs:
            metadata = {'id': vec.resume_id, 'score': cosine_similarity(vec.cv_vector, self.prompt.cv_vector)}
            results.append(
                InterpretableVector(
                    vec, 
                    self.prompt, 
                    metadata=metadata
                )
            )

        results.sort(reverse=True)
        return results[:top_n]

    def get_sorted_metadata(self) -> list[dict]:
        cvs = self.sort_cvs()
        return [cv.metadata for cv in cvs]

    def get_full_result(self) -> list[tuple[dict, tuple[list[str], list[str]]]]:
        cvs = self.sort_cvs()
        return [(cv.metadata, cv.get_positive_negative_words()) for cv in cvs]


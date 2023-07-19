from typing import Dict
from typing import Tuple
from typing import List

from vectorizer import Vector
from metrics import cosine_similarity


class InterpretableVector:
    def __init__(self, text: str or Vector, prompt: str or Vector, threshold: float = 0.9, cache_importance: bool = True, metadata: dict = None):
        if isinstance(text, str):
            text = Vector(-1, text, do_preprocess=False)
        if isinstance(prompt, str):
            prompt = Vector(-1, prompt, do_preprocess=True)

        self.resume = text
        self.prompt = prompt
        self.importance = dict()
        self.threshold = threshold
        self.cache_importance = cache_importance
        self.metadata = metadata  # dict{id, score}

    def analyze_word_importance(self) -> Dict[str, float]:
        words, embeddings = self.resume.get_words_embeddings()
        importance = self.importance if self.cache_importance else dict()
        for word, emb in zip(words, embeddings):
            importance[word] = cosine_similarity(self.prompt.cv_vector, emb)
        return importance

    def get_sorted_words(self) -> List[Tuple[str, float]]:
        return sorted(self.importance.items(), key=lambda a: a[1], reverse=True)

    def get_positive_negative_words(self) -> Tuple[List[str], List[str]]:
        positive, negative = [], []
        for word, score in self.importance.items():
            if score >= self.threshold:
                positive.append(word)
            elif score <= -self.threshold:
                negative.append(word)
        return positive, negative

    def __eq__(self, other):
        other: InterpretableVector
        if self.metadata is not None and other.metadata is not None:
            return self.metadata.get('score', -10) == other.metadata.get('score', -10)
        return False

    def __gt__(self, other):
        other: InterpretableVector
        if self.metadata is not None and other.metadata is not None:
            return self.metadata.get('score', -10) > other.metadata.get('score', -10)
        return self.metadata is not None

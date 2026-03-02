import math
from typing import List, Tuple


class VectorStore:
    def __init__(self):
        self.vectors: List[Tuple[str, List[float], str]] = []

    def add(self, doc_id: str, text: str, embedding: List[float]):
        self.vectors.append((doc_id, embedding, text))

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = math.sqrt(sum(pow(a, 2) for a in v1))
        norm_v2 = math.sqrt(sum(pow(b, 2) for b in v2))

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return dot_product / (norm_v1 * norm_v2)

    def search(self, query_embedding: List[float], top_k: int = 3):
        scored = []
        if not self.vectors:
            return []

        for doc_id, embedding, text in self.vectors:
            score = self.cosine_similarity(query_embedding, embedding)
            scored.append((score, doc_id, text))

        scored.sort(reverse=True, key=lambda x: x[0])

        return scored[:top_k]

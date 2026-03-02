import faiss
import os
from app.models.models import Document
import json
import numpy as np
from typing import List, Tuple


class FAISSVectorStore:

    def __init__(self, dimension: int):
        self.dimension = dimension
        if os.path.exists("faiss.index"):
            self.index = faiss.read_index("faiss.index")
            if self.index.d != self.dimension:
                raise ValueError(f"Index dimension {self.index.d} does not match expected {self.dimension}")
        else:
            self.index = faiss.IndexFlatIP(dimension)

        if os.path.exists("docs.json"):
            with open("docs.json") as f:
                self.texts = json.load(f)
        else:
            self.texts: List[Tuple[str, str, str]] = []  # doc_id, title and text

    def add(self, doc_id: str, title: str, text: str, embedding: List[float]):
        vector = np.array([embedding], dtype="float32")

        self.index.add(vector)
        self.texts.append((doc_id, title, text))

    def save(self):
        faiss.write_index(self.index, "faiss.index")
        with open("docs.json", "w") as f:
            json.dump(self.texts, f, ensure_ascii=False, indent=2)

    def search(self, query_embedding: List[float], top_k: int = 3):
        if self.index.ntotal == 0:
            return []

        query = np.array([query_embedding], dtype="float32")
        scores, indices = self.index.search(query, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            doc_id, title, text = self.texts[idx]
            results.append((float(score), doc_id, title, text))

        return results

    def document_exists(self, doc_id: str) -> bool:
        return any(existing_id == doc_id for existing_id, _, _ in self.texts)

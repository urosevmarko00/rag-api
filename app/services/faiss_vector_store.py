import faiss
import os
import json
import numpy as np
from typing import List, Tuple
from app.core.logger import get_logger

logger = get_logger(__name__)


class FAISSVectorStore:

    def __init__(self, dimension: int):
        self.dimension = dimension

        self.data_dir = "data"
        self.faiss_path = os.path.join(self.data_dir, "faiss.index")
        self.docs_path = os.path.join(self.data_dir, "docs.json")

        if os.path.exists(self.faiss_path):
            self.index = faiss.read_index(self.faiss_path)
            logger.info("FAISS index loaded from disk")
            if self.index.d != self.dimension:
                raise ValueError(f"Index dimension {self.index.d} does not match expected {self.dimension}")
        else:
            self.index = faiss.IndexFlatIP(dimension)
            logger.info("New FAISS index created")

        if os.path.exists(self.docs_path):
            with open(self.docs_path) as f:
                self.texts = json.load(f)
                logger.info(f"Loaded {len(self.texts)} stored chunks")
        else:
            self.texts: List[Tuple[str, str, str]] = []  # doc_id, title and text
            logger.info("No existing documents found")

    def add(self, doc_id: str, title: str, text: str, embedding: List[float]):
        vector = np.array([embedding], dtype="float32")

        self.index.add(vector)
        self.texts.append((doc_id, title, text))

        logger.debug(f"Added chunk for document {doc_id}")

    def save(self):
        faiss.write_index(self.index, self.faiss_path)
        with open(self.docs_path, "w", encoding="utf-8") as f:
            json.dump(self.texts, f, ensure_ascii=False, indent=2)
        logger.info(f"FAISS index saved. Total vectors: {self.index.ntotal}")

    def search(self, query_embedding: List[float], top_k: int = 3):
        if self.index.ntotal == 0:
            logger.info("Search attempted on empty index")
            return []

        query = np.array([query_embedding], dtype="float32")
        scores, indices = self.index.search(query, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            doc_id, title, text = self.texts[idx]
            results.append((float(score), doc_id, title, text))

        logger.debug(f"Search returned {len(results)} results")

        return results

    def document_exists(self, doc_id: str) -> bool:
        return any(existing_id == doc_id for existing_id, _, _ in self.texts)

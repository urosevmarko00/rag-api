from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(text, convert_to_numpy=True)

        norm = np.linalg.norm(embedding)
        if norm != 0:
            embedding = embedding/norm

        return embedding.tolist()

    def get_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

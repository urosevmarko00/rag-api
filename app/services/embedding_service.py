import hashlib


class EmbeddingService:

    def embed(self, text: str) -> list[float]:
        hash_object = hashlib.sha256(text.encode())
        hash_digest = hash_object.digest()

        embedding = [b / 255 for b in hash_digest[:10]]

        return embedding

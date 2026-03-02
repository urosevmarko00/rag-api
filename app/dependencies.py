from app.services.rag_service import RAGService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.chunking_service import ChunkingService
from app.services.faiss_vector_store import FAISSVectorStore
from app.core.config import settings


embedding = EmbeddingService()
vector_store = FAISSVectorStore(embedding.get_dimension())
chunking = ChunkingService()
rag_service = RAGService(embedding, vector_store, chunking)


def get_rag_service():
    return rag_service


def get_api_version():
    return settings.api_version

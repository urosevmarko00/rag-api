from app.services.rag_service import RAGService
from app.core.config import settings

rag_service = RAGService()


def get_rag_service():
    return rag_service


def get_api_version():
    return settings.api_version

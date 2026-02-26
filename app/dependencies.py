from app.services.rag_service import RAGService
from app.core.config import settings


def get_rag_service():
    return RAGService()


def get_api_version():
    return settings.api_version

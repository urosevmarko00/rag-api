from fastapi import APIRouter, Depends
from app.models import models
from app.services.rag_service import RAGService
from app import dependencies

router = APIRouter()


@router.post("/document")
def create_document(doc: models.Document, rag_service: RAGService = Depends(dependencies.get_rag_service)):
    rag_service.add_document(doc)
    return {"message": "Document added"}

from fastapi import APIRouter, Depends, HTTPException
from app.models import models
from app.services.rag_service import RAGService
from app import dependencies

router = APIRouter()


@router.post("/document")
def create_document(doc: models.Document, rag_service: RAGService = Depends(dependencies.get_rag_service)):
    try:
        rag_service.add_document(doc)
        return {"message": "Document added"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

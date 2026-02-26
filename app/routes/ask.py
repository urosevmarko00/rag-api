from fastapi import APIRouter, Depends, HTTPException
from app.models import models
from app.services.rag_service import RAGService
from app import dependencies

router = APIRouter()


# region POSTS

@router.post("/ask")
def ask_question(request: models.QuestionRequest, rag_service: RAGService = Depends(dependencies.get_rag_service)):
    return rag_service.ask(request.question)


# endregion

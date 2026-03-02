from fastapi import APIRouter, Depends, HTTPException
from app.models import models
from app.services.rag_service import RAGService
from app import dependencies

router = APIRouter()


# region POSTS

@router.post("/ask")
def ask_question(request: models.QuestionRequest, top_k: int = 3, rag_service: RAGService = Depends(dependencies.get_rag_service)):
    try:
        result = rag_service.ask(request.question, top_k)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion

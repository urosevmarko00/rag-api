from fastapi import APIRouter
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


router = APIRouter()


@router.post("/ask")
def ask_question(request: QuestionRequest):
    return {"received": request}

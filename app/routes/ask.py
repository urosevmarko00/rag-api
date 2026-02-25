from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# region POSTS
class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):
    return {"received": request}
# endregion

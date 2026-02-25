from fastapi import APIRouter
from app.models import models

router = APIRouter()


# region POSTS

@router.post("/ask")
def ask_question(request: models.QuestionRequest):
    return {"received": request.question}
# endregion

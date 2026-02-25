from pydantic import BaseModel, Field, StrictStr


class QuestionRequest(BaseModel):
    question: StrictStr


class Document(BaseModel):
    title: StrictStr
    content: StrictStr = Field(min_length=10)

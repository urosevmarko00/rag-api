from pydantic import BaseModel, Field, StrictStr


class QuestionRequest(BaseModel):
    question: StrictStr = Field(min_length=3, max_length=2000)


class Document(BaseModel):
    title: StrictStr
    content: StrictStr = Field(min_length=10)

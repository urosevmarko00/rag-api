from fastapi import FastAPI
from fastapi import Depends
from app.routes import health, ask
from pydantic import BaseModel, Field


class Document(BaseModel):
    title: str
    content: str = Field(min_length=10)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


app.include_router(health.router)
app.include_router(ask.router)


def get_api_version():
    return "v1"


@app.get("/version")
def version(api_version: str = Depends(get_api_version)):
    return {"version": api_version}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}


@app.post("/documents")
def create_document(doc: Document):
    return {"message": "Document stored", "length": len(doc.title + doc.content)}

from fastapi import FastAPI
from fastapi import Depends
from app.routes import health, ask
from app.models import models
from app.core.config import settings
from pydantic import BaseModel, Field

app = FastAPI()


# region GETS
@app.get("/")
def root():
    return {"message": "FastAPI is running"}


app.include_router(health.router)


def get_api_version():
    return settings.api_version


@app.get("/version")
def version(api_version: str = Depends(get_api_version)):
    return {"version": api_version}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}


# endregion

# region POSTS


@app.post("/documents")
def create_document(doc: models.Document):
    return {"message": "Document stored", "length": len(doc.title + doc.content)}


app.include_router(ask.router)

# endregion

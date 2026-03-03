from fastapi import FastAPI
from fastapi import Depends
from app.routes import health, ask, document
from app import dependencies
from app.core.logger import setup_logger

setup_logger()
app = FastAPI()


# region GETS
@app.get("/")
def root():
    return {"message": "FastAPI is running"}


app.include_router(health.router)


@app.get("/version")
def version(api_version: str = Depends(dependencies.get_api_version)):
    return {"version": api_version}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}


# endregion

# region POSTS

app.include_router(document.router)
app.include_router(ask.router)

# endregion

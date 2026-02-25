from fastapi import APIRouter

router = APIRouter()


# region GETS
@router.get("/health")
def health():
    return {"status": "ok"}
# endregion

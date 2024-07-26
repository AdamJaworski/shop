from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from config import HTML_DIR

router = APIRouter()


@router.get("/")
async def root():
    with open(HTML_DIR + "/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@router.get("/items")
async def get_items():
    return {"message": "List of items"}

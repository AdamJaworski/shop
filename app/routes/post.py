from fastapi import APIRouter, Request
from config import HTML_DIR

router = APIRouter()


@router.post("/items")
async def create_item(request: Request):
    return {"message": "Item created"}

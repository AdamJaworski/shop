from fastapi import APIRouter, Request
from config import HTML_DIR

router = APIRouter()


@router.post("/get_cart")
async def create_item(request: Request):
    return {"message": "Item created"}

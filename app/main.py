from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.get import router as get
from app.routes.post import router as post
from config import *
app = FastAPI()

app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")

app.include_router(get)
app.include_router(post)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
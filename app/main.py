from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.get import router as get
from app.routes.post import router as post

app = FastAPI()

app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/icons", StaticFiles(directory="templates/icons"), name="icons")

app.include_router(get)
app.include_router(post)

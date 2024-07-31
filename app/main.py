from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.get import router as get
from app.routes.post import router as post
from app.routes.items_get import router as items_get, init_item_routes
from config import *
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # init shop items
    init_item_routes()
    app.include_router(items_get)
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")

app.include_router(get)
app.include_router(post)


if __name__ == "__main__":
    import subprocess
    subprocess.call(r'C:\Users\Adam\AppData\Roaming\npm\pug.cmd -o templates/html templates/pug', shell=True)

    import uvicorn
    uvicorn.run(app, host="localhost", port=80)


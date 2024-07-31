import threading

from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from app.routes.get import router as get
from app.routes.post import router as post
from app.routes.items_get import router as items_get, init_item_routes
from config import *
from contextlib import asynccontextmanager
import asyncio
from fastapi.responses import JSONResponse


def init_and_add_routes():
    init_item_routes()
    app.include_router(items_get)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init shop
    threading.Thread(target=init_and_add_routes).start()
    yield

app = FastAPI(lifespan=lifespan) #

app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")

app.include_router(get)
app.include_router(post)

@app.post("/debug/refresh-docs")
async def refresh_docs():
    app.openapi_schema = None
    app.openapi()
    return JSONResponse(content={'status': True}, status_code=200)


# @app.post("/initialize-routes")
# async def initialize_routes():
#     init_item_routes()
#     app.include_router(items_get)
#     return JSONResponse(content={'status': True}, status_code=200)




if __name__ == "__main__":
    import subprocess
    subprocess.call(r'C:\Users\Adam\AppData\Roaming\npm\pug.cmd -o templates/html templates/pug', shell=True)

    import uvicorn
    uvicorn.run(app, host="localhost", port=80)


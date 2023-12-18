# 테스트 DB 생성
#######################
from src.adapters.api.create_db import create_db_function
# initialized the test dataset :)
create_db_function()
#######################

from fastapi import FastAPI
from src.adapters.api import rec_router, create_db, point_router
from src.infrastructure.queue.task_queue import task_queue, worker_task
from threading import Thread


app = FastAPI()

@app.get("/")
def index():
    return {"title": "This is Working :)"}
# @app.get("/")
# async def rerec_root():
#     return {"message": "Hello World"}
# @app.get("/hello")
# async def hello_root():
#     return {"message": "Hello World"}

app.include_router(rec_router.router, prefix="/recs", tags=["recs"])
app.include_router(point_router.router, prefix="/point", tags=["point"])
app.include_router(create_db.router, prefix="/db", tags=["db"])

worker_thread = Thread(target=worker_task, args=(task_queue,))
worker_thread.daemon = True
worker_thread.start()

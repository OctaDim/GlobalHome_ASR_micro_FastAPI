import asyncio
import threading

import uvicorn
from fastapi import FastAPI

from configs.settings import API_CONFIGS
from fast_api.app_vosk.routers_vosk import router_vosk


def create_fastapi_app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(router_vosk)
    return fastapi_app


def run_uvicorn_fastapi_server():
    uvicorn.run(app=create_fastapi_app(),
                # app="main:create_fastapi_app",  # literal func call is necessary if server reload=True when code changing
                host=API_CONFIGS.BASE_HOST,
                port=API_CONFIGS.BASE_PORT,
                # reload=True,
                # factory=True,
                use_colors=True)
    print("Uvicorn and FastAPI started")


async def run_task_1():
    while True:
        print("Additional 1 started")
        await asyncio.sleep(5)


async def run_task_2():
    while True:
        print("Additional 2 started")
        await asyncio.sleep(15)


async def run_task_3():
    while True:
        print("Additional 3 started")
        await asyncio.sleep(30)



async def run_tasks():
    task_1 = asyncio.create_task(run_task_1())
    task_2 = asyncio.create_task(run_task_2())
    task_3 = asyncio.create_task(run_task_3())
    await asyncio.gather(task_1, task_2, task_3)

if __name__ == "__main__":
    uvicorn_server_thread = threading.Thread(
        target=run_uvicorn_fastapi_server, daemon=True)
    uvicorn_server_thread.start()

    asyncio.run(run_tasks())

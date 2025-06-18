import asyncio

from fastapi import FastAPI
from uvicorn import Config, Server

from configs.settings import API_HOST, API_PORT
from fast_api.app_vosk.routers_vosk import router_vosk


def create_fastapi_app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(router_vosk)
    return fastapi_app


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


async def run_main():
    uvicorn_fastapi_config = Config(app=create_fastapi_app(),
                                    # app="main:create_fastapi_app",  # literal func call is necessary if server reload=True when code changing
                                    host=API_HOST,
                                    port=API_PORT,
                                    # reload=True,
                                    # factory=True,
                                    use_colors=True)
    print("Uvicorn and FastAPI started")

    uvicorn_fastapi_server = Server(uvicorn_fastapi_config)

    task_1 = asyncio.create_task(run_task_1())
    task_2 = asyncio.create_task(run_task_2())
    task_3 = asyncio.create_task(run_task_3())
    uvicorn_fastapi_server_task = uvicorn_fastapi_server.serve()

    await asyncio.gather(uvicorn_fastapi_server_task,
                         task_1, task_2, task_3)


if __name__ == "__main__":
    asyncio.run(run_main())

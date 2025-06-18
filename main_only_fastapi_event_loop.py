import uvicorn
from fastapi import FastAPI

from configs.settings import API_HOST, API_PORT
from fast_api.app_vosk.routers_vosk import router_vosk


def create_fastapi_app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(router_vosk)
    return fastapi_app


async def run_uvicorn_fastapi_server():
    uvicorn.run(app=create_fastapi_app(),
                # app="main:create_fastapi_app",  # literal func call is necessary if server reload=True when code changing
                host=API_HOST,
                port=API_PORT,
                # reload=True,
                # factory=True,
                use_colors=True)
    print("Uvicorn and FastAPI server started")


if __name__ == "__main__":
    run_uvicorn_fastapi_server()

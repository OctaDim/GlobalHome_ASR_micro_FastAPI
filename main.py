import uvicorn
from fastapi import FastAPI

from configs.settings import API_CONFIGS
from fast_api.app_root_url.router_main import router_root_url
from fast_api.app_vosk.routers_vosk import router_vosk


def create_fastapi_application():
    fastapi_app = FastAPI()
    fastapi_app.include_router(router_root_url)
    fastapi_app.include_router(router_vosk)
    return fastapi_app


def run_uvicorn_fastapi_server():
    uvicorn.run(app=create_fastapi_application(),
                # app="main:create_fastapi_app",  # literal func call is necessary if server reload=True when code changing
                host=API_CONFIGS.BASE_HOST,
                port=API_CONFIGS.BASE_PORT,
                # reload=True,
                # factory=True,
                use_colors=True,)
    print("Uvicorn and FastAPI server started")


if __name__ == "__main__":
    run_uvicorn_fastapi_server()

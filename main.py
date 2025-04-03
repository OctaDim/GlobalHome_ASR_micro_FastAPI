import uvicorn
from fastapi import FastAPI

from configs.settings import API_CONFIGS
from fast_api_apps.fastapi_app_vosk.routers_vosk import router_vosk


def create_fastapi_app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(router_vosk)
    return fastapi_app


if __name__ == "__main__":
    import_fastapi_app = "main:create_fastapi_app"
    uvicorn.run(app=import_fastapi_app,
                host=API_CONFIGS.BASE_HOST,
                port=API_CONFIGS.BASE_PORT,
                use_colors=True,
                reload=True)

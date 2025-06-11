from typing import Annotated

from aiofiles import os as aios
from fastapi import Body, HTTPException, status

from configs.settings import API_DEFAULT_PASSWORD, API_DEFAULT_USERNAME
from fast_api.app_vosk.schemes_vosk import AuthBaseModel


def verify_auth_data(auth: Annotated[AuthBaseModel, Body(..., embed=True)]) -> str:
    if (auth.username != API_DEFAULT_USERNAME
            or auth.password != API_DEFAULT_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication [ERROR]: invalid credentials",
            headers={"WWW-Authenticate": "Basic"}, )

    log_text = f"Authentication [OK]: username: {auth.username}"
    print(log_text)
    return auth.username


async def async_remove_file(full_file_path: str) -> None:
    if await aios.path.exists(full_file_path):
        await aios.remove(full_file_path)

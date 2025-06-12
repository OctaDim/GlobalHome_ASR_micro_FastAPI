from typing import Annotated

from fastapi import Body, HTTPException
from starlette import status

from configs.settings import API_ENV_PASSWORD, API_ENV_USERNAME
from fast_api.auth_app.schemes_auth import AuthBaseModel


def verify_auth_data(auth: Annotated[AuthBaseModel, Body(..., embed=True)]) -> str:
    if (auth.username != API_ENV_USERNAME
            or auth.password != API_ENV_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Authentication [ERROR]: invalid credentials",
            headers={"WWW-Authenticate": "Basic"}, )

    log_text = f"API Authentication [OK]: username: {auth.username}"
    print(log_text)
    return auth.username

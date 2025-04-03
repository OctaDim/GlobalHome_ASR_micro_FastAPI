from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, model_validator

from configs.creds_from_env import API_DEFAULT_LOGIN, API_DEFAULT_PASSWORD


class LogPassPydantic(BaseModel):
    login: str
    password: str

    @field_validator("login")
    def validate_username(cls, value: str) -> str | HTTPException:
        if not value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing or empty login")
        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str | HTTPException:
        if not value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing or empty password")
        return value

    @model_validator(mode="after")
    def check_logger_name(self) -> "LogPassPydantic":
        if (self.login != API_DEFAULT_LOGIN
                or self.password != API_DEFAULT_PASSWORD):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login or password")
        return self


class LogPassErrorPydantic(BaseModel):
    detail: str

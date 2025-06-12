from pydantic import BaseModel


class AuthBaseModel(BaseModel):
    username: str
    password: str

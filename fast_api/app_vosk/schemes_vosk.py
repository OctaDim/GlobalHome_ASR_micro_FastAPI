from pydantic import BaseModel


class AuthBaseModel(BaseModel):
    username: str
    password: str

# class AuthType(TypedDict):
#     username: str
#     password: str
#
#
# class AuthBaseModel(BaseModel):
#     auth: AuthType

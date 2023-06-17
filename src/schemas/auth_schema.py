from pydantic import BaseModel


class Auth(BaseModel):
    account: str
    password: str

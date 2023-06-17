from pydantic import BaseModel


class UserBase(BaseModel):
    email: str | None
    username: str | None


class UserCreate(UserBase):
    password: str
    password_confirm: str


class User(UserBase):
    userId: int | None

    class Config:
        orm_mode = True

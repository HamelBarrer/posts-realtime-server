from pydantic import BaseModel

from . import user_schema


class PostBase(BaseModel):
    title: str
    description: str | None


class PostCreate(PostBase):
    user_id: int


class Post(PostBase):
    post_id: int
    user: user_schema.User

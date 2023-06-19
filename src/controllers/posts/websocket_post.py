from fastapi import HTTPException

from ...services import posts_service
from ...schemas import posts_schema


async def get_posts():
    data = await posts_service.read_posts()
    if len(data) == 0:
        raise HTTPException(status_code=204, detail='Not posts')

    return data


async def create_post(post: posts_schema.PostCreate):
    data = await posts_service.insert_post(post)

    return data

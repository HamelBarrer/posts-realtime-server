from fastapi import APIRouter, HTTPException

from ..services import posts_service
from ..schemas import posts_schema

router = APIRouter(
    prefix='/api/v1/posts'
)


@router.get('/{post_id}', response_model=posts_schema.Post)
async def get_post(post_id: int):
    data = await posts_service.read_post(post_id)
    if data is None:
        raise HTTPException(status_code=404, detail='Post not found')

    return data


@router.get('/', response_model=list[posts_schema.Post])
async def get_posts():
    data = await posts_service.read_posts()
    if len(data) == 0:
        raise HTTPException(status_code=204, detail='Not posts')

    return data


@router.post('/', response_model=posts_schema.Post)
async def create_post(post: posts_schema.PostCreate):
    data = await posts_service.insert_post(post)

    return data

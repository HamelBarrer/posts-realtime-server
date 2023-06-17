from typing import List
from fastapi import APIRouter, HTTPException

from ..schemas import user_schema
from ..services import user_service

router = APIRouter(
    prefix='/api/v1/users'
)


@router.get('/{user_id}', response_model=user_schema.User)
async def get_user(user_id: int):
    data = await user_service.read_user(user_id)
    if data is None:
        raise HTTPException(status_code=404, detail='User not found')

    return data


@router.get('/', response_model=List[user_schema.User])
async def get_user():
    data = await user_service.read_users()
    if len(data) == 0:
        raise HTTPException(status_code=204, detail='Not users')

    return data


@router.post('/', response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate):
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail='The password not equals')

    data = await user_service.insert_user(user)

    return data

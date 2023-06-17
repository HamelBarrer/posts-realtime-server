from fastapi import APIRouter, HTTPException

from ..schemas import auth_schema
from ..services import user_service
from ..utils import hash, token_util

router = APIRouter(
    prefix='/api/v1/auth'
)


@router.post('/')
async def login(auth: auth_schema.Auth):
    user = await user_service.read_user_by_account(auth.account)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail='Account or Password incorrect'
        )

    if not hash.verify_hash(auth.password, user.password):
        raise HTTPException(
            status_code=400,
            detail='Account or Password incorrect'
        )

    token = token_util.creation_token({'user_id': str(user.userId)})

    data = {
        'user_id': user.userId,
        'email': user.email,
        'username': user.username,
        'token': token
    }

    return {'data': data}

from typing_extensions import Annotated
from fastapi import Depends, HTTPException

from ..services import user_service
from ..utils import token_util
from ..schemas import user_schema


async def get_current_user(token: Annotated[str, Depends(token_util.oauth_schema)]):
    user_id = token_util.validate_token(token)
    user = await user_service.read_user(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail='Token invalid')

    return user

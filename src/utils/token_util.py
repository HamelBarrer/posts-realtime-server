from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from .. import config

oauth_schema = OAuth2PasswordBearer(tokenUrl='token')


def creation_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def validate_token(token: str):
    payload = jwt.decode(
        token,
        config.SECRET_KEY,
        algorithms=[config.ALGORITHM]
    )
    return payload.get('user_id')

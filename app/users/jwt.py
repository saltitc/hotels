from datetime import datetime, timedelta
from enum import Enum
import time

from jose import JWTError, jwt

from app.users.config import auth_config
from app.users.dao import UsersDAO
from app.users.exceptions import (
    IncorrectTokenFormatException,
    TokenExpiredException,
)
from app.users.models import Users


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


def _create_token(user: Users, token_type: TokenType) -> str:
    minutes = auth_config.ACCESS_TOKEN_EXPIRE_MINUTES
    secret = auth_config.ACCESS_TOKEN_SECRET
    if token_type == TokenType.REFRESH:
        minutes = auth_config.REFRESH_TOKEN_EXPIRE_MINUTES
        secret = auth_config.REFRESH_TOKEN_SECRET
    expires = datetime.utcnow() + timedelta(minutes=minutes)
    data = {
        "user_id": user.id,
        "username": user.username,
        "token_type": token_type,
        "expires": expires.isoformat(),
    }
    encoded_token = jwt.encode(data, key=secret, algorithm=auth_config.ALGORITHM)
    exp = time.strftime('%a, %d-%b-%Y %T GMT', time.gmtime(time.time() + minutes))
    return {"token": encoded_token, "expires": exp}


def create_access_token(user: Users) -> str:
    return _create_token(user, TokenType.ACCESS)


def create_refresh_token(user: Users) -> str:
    return _create_token(user, TokenType.REFRESH)


def create_tokens(user: Users) -> dict[str, str]:
    access = create_access_token(user)
    refresh = create_refresh_token(user)

    return {
        TokenType.ACCESS.value: access,
        TokenType.REFRESH.value: refresh,
    }


def parse_token(
    token: str,
    token_type: TokenType,
) -> dict:
    secret = (
        auth_config.ACCESS_TOKEN_SECRET
        if token_type == TokenType.ACCESS
        else auth_config.REFRESH_TOKEN_SECRET
    )
    try:
        payload = jwt.decode(
            token=token,
            key=secret,
            algorithms=auth_config.ALGORITHM,
        )

        user_id = payload.get("user_id")
        username = payload.get("username")
        expires = payload.get("expires")
        token_type_payload = payload.get("token_type")
    except JWTError:
        raise IncorrectTokenFormatException

    correct = token_type_payload == token_type.value
    expired = datetime.fromisoformat(expires) < datetime.utcnow()
    if not correct:
        raise JWTError
    if expired:
        raise TokenExpiredException

    return {
        "user_id": user_id,
        "username": username,
        "expires": expires,
        "token_type": token_type,
    }


async def refresh_tokens(refresh_token: str) -> dict[str]:
    token_data = parse_token(refresh_token, TokenType.REFRESH)
    user = await UsersDAO.find_by_id(token_data["user_id"])
    return {"user": user, **create_tokens(user)}

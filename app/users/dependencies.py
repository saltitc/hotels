from fastapi import Depends, Request
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)

from app.users.dao import UsersDAO
from app.users.jwt import TokenType, parse_token


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    token_data = parse_token(
        token=token, token_type=TokenType.ACCESS
    )
    user_id: str = token_data["user_id"]
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user

from fastapi import APIRouter, Depends, Response
from app.users.auth import (
    authenticate_user,
    get_password_hash,
    password_equality,
)
from app.users.dependencies import get_current_user
from app.users.exceptions import (
    PasswordsAreNotEqualException,
    UserAlreadyExistsException,
)
from app.users.jwt import refresh_tokens
from app.users.models import Users
from app.users.schemas import RefreshToken, UserRegisterSchema, UserLoginSchema
from app.users.dao import UsersDAO

router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/register")
async def register_user(user_data: UserRegisterSchema):
    user = await UsersDAO.get_user(
        username=user_data.username,
        email=user_data.email,
    )
    if user:
        raise UserAlreadyExistsException
    if not password_equality(user_data.password1, user_data.password2):
        raise PasswordsAreNotEqualException
    password_hash = get_password_hash(user_data.password1)
    return await UsersDAO.create_user(
        username=user_data.username, email=user_data.email, password=password_hash
    )


@router.post("/login")
async def login_user(response: Response, user_data: UserLoginSchema):
    user_data = await authenticate_user(user_data.username, user_data.password)
    response.set_cookie(
        "booking_access_token", user_data["access_token"], httponly=True
    )
    response.set_cookie(
        "booking_refresh_token", user_data["refresh_token"], httponly=True
    )
    return "Вы авторизованы"


@router.post("/refresh")
async def refresh(response: Response, refresh_token: RefreshToken):
    user_data = await refresh_tokens(refresh_token.refresh_token)
    response.set_cookie(
        "booking_access_token", user_data["access_token"], httponly=True
    )
    response.set_cookie(
        "booking_refresh_token", user_data["refresh_token"], httponly=True
    )
    return "Токены обновлены"


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    response.delete_cookie("booking_refresh_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}

from passlib.context import CryptContext
from pydantic import EmailStr

from app.users.dao import UsersDAO
from app.users.exceptions import IncorrecUsernameOrPasswordException
from app.users.jwt import create_tokens

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def password_equality(password1: str, password2: str) -> bool:
    return password1 == password2


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await UsersDAO.get_user(username=username)
    if not user or not verify_password(password, user.password):
        raise IncorrecUsernameOrPasswordException
    return {"user": user, **create_tokens(user)}

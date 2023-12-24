from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str

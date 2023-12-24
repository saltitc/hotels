from passlib.context import CryptContext
from pydantic import Field
from pydantic import BaseSettings
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 30)  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 60 * 24 * 7)  # 7 days

    ACCESS_TOKEN_SECRET: str = Field(default=settings.SECRET_KEY + "_access")
    REFRESH_TOKEN_SECRET: str = Field(default=settings.SECRET_KEY + "_refresh")
    
    ALGORITHM: str = Field(default=settings.ALGORITHM)


auth_config = AuthSettings()

from typing import Literal
from pydantic import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    
    ALGORITHM: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    ALGORITHM: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

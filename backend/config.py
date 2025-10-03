# backend/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Add this line
    DATABASE_URL: str
    CORS_ORIGINS: str

    # Keep all the mail settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    class Config:
        env_file = "backend/.env"

settings = Settings()
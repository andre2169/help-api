from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./help_api.db"

    class Config:
        env_file = ".env"


settings = Settings()

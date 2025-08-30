from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # These are optional because Railway uses DATABASE_URL
    database_hostname: str | None = None
    database_port: str | None = None
    database_password: str | None = None
    database_name: str | None = None
    database_username: str | None = None

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()

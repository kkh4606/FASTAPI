from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str | None = None  # Add this for Railway
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

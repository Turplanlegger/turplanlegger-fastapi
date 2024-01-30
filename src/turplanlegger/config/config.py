from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URI: str = Field(min_length=1)
    DATABASE_MAX_RETRIES: int = Field(5)

    # Logging
    CORS_ORIGINS: list = Field(['http://localhost:3000'])

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', env_prefix='TP_')
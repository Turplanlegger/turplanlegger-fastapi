"""
Settings: Field Value Priority
In the case where a value is specified for the same Settings field in multiple ways,
the selected value is determined as follows (in descending order of priority):

Arguments passed to the Settings class initialiser.
Environment variables, e.g. TP_VARIABLENAME.
Variables loaded from a dotenv (.env) file.
Variables loaded from the secrets directory.
The default field values for the Settings model.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    # postgresql+psycopg tells SQLModel/SQLAlchemy to use psycopg(3) instead of psycopg2
    DATABASE_URI: str = Field(
        'postgresql+psycopg://turadm:passord@localhost:5432/turplanlegger?connect_timeout=10&application_name=turplanlegger-fastapi',
        min_length=1,
    )
    DATABASE_MAX_RETRIES: int = Field(5)
    DATABASE_DEBUG: bool = Field(False)

    # CORS
    CORS_ORIGINS: list = Field(['http://localhost:3000'])

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix='TP_')


@lru_cache
def get_settings():
    return Settings()

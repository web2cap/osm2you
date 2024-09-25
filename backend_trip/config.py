from typing import Literal

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    ST_SECRET_KEY: str

    model_config = ConfigDict(env_file=".env", extra="allow")


settings = Settings()

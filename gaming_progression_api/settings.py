from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(
    BaseSettings,
):
    project_name: str
    debug: bool
    database_url: str
    jwt_secret: str
    jwt_algoritm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file='.env', env_prefix='API_')


@lru_cache
def get_settings() -> Settings:
    return Settings()
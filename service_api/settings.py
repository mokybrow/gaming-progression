from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(
    BaseSettings,
):
    project_name: str
    debug: bool
    db_url: str

    model_config = SettingsConfigDict(env_prefix='API_', env_file='.env')


@lru_cache
def get_settings() -> Settings:
    return Settings()

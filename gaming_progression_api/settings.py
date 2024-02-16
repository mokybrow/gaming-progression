from functools import lru_cache
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(override=True)

class Settings(
    BaseSettings,
):
    project_name: str
    debug: bool
    database_url2: str
    jwt_secret: str
    jwt_algoritm: str
    access_token_expire_minutes: int
    verify_token_expire_minutes: int
    reset_token_expire_minutes: int
    auth_audience: str
    verify_audience: str
    reset_audience: str
    MODE:str

    model_config = SettingsConfigDict(env_file='.env', env_prefix='API_')


@lru_cache
def get_settings() -> Settings:
    return Settings()

from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


class Settings(
    BaseSettings,
):
    MODE: str
    project_name: str
    debug: bool
    database_url: str
    jwt_secret: str
    jwt_algoritm: str
    access_token_expire_minutes: int
    verify_token_expire_minutes: int
    reset_token_expire_minutes: int
    auth_audience: str
    verify_audience: str
    reset_audience: str

    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str
    front_host: str

    s3_id: str
    s3_key: str
    redis_host: str
    redis_port: int
    model_config = SettingsConfigDict(env_file='.env', env_prefix='API_')


@lru_cache
def get_settings() -> Settings:
    return Settings()

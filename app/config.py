import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.logger import get_logger

logger = get_logger(__name__)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="", env_file_encoding='utf-8',case_sensitive=True)
    
    ENV: str

    POSTGRES_DRIVER_NAME: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    SERVICE_ACCOUNT_FILE: str

class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file="./.env.test", env_file_encoding='utf-8',case_sensitive=True)

    ENV: str = 'test'

class LocalSettings(Settings):
    model_config = SettingsConfigDict(env_file='./.env.local', env_file_encoding='utf-8', case_sensitive=True)

    ENV: str = 'local'

class DevSettings(Settings):
    model_config = SettingsConfigDict(env_file='./.env.dev', env_file_encoding='utf-8', case_sensitive=True)

    ENV: str = 'dev'

def get_settings(env: str = 'dev') -> Settings:
    try:
        if env.lower() == 'test':
            return TestSettings()
        elif env.lower() == 'local':
            return LocalSettings()
        elif env.lower() == 'dev':
            return DevSettings()
    except Exception:
        logger.exception(f'Failed to load settings for environment {env}')
        raise

_env = os.environ.get("ENV", "local")
settings = get_settings(env=_env)
logger.info(f'Loaded {settings.ENV} environment settings')
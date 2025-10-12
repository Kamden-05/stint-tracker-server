from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="", env_file_encoding='utf-8',case_sensitive=True)
    
    ENV: str

    POSTGRES_DRIVER_NAME: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

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
    if env.lower() == 'test':
        return TestSettings()
    elif env.lower() == 'local':
        return LocalSettings()
    elif env.lower() == 'dev':
        return DevSettings()
    
    raise ValueError("Invalid Environment. Must be 'test', 'local', or 'dev'")
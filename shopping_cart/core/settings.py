import os
from functools import lru_cache
from pydantic import BaseSettings

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"

class EnvironmentSettings(BaseSettings):
    
    APP_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    CLUSTER_NAME: str
    RETRY: str
    W: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()



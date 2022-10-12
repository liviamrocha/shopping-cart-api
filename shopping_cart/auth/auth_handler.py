from decouple import config
from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_ALGORITHM: str =  config("JWT_ALGORITHM", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 200
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True

settings_auth = Settings()
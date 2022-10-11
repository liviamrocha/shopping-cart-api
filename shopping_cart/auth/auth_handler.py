import time
from typing import Dict

import jwt
from decouple import config
from pydantic import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY = config("secret")
    JWT_ALGORITHM = config("algorithm")
    JWT_REFRESH_SECRET_KEY = config("refresh_secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True

settings = Settings()


def token_response(token: str):
    return {
        "access_token": token
    }
    
    
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
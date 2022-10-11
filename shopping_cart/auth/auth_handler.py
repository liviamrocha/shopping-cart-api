from decouple import config
from pydantic import BaseSettings
from decouple import config
from shopping_cart.core import settings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_ALGORITHM: str =  config("JWT_ALGORITHM", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True

settings_auth = Settings()


# def token_response(token: str):
#     return {
#         "access_token": token
#     }
    
    
# def signJWT(email: str) -> Dict[str, str]:
#     payload = {
#         "email": email,
#         "expires": time.time() + 600
#     }
#     token = jwt.encode(payload, settings_auth.JWT_SECRET_KEY, algorithm=settings_auth.JWT_ALGORITHM)

#     return token_response(token)


# def decodeJWT(token: str) -> dict:
#     try:
#         decoded_token = jwt.decode(token, settings_auth.JWT_SECRET_KEY, algorithms=[settings_auth.JWT_ALGORITHM])
#         return decoded_token if decoded_token["expires"] >= time.time() else None
#     except:
#         return {}
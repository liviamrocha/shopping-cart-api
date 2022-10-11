from pydantic import BaseModel, EmailStr

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: EmailStr = None
    exp: int = None
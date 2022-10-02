from datetime import datetime
from time import sleep
from email.policy import default
from pydantic import BaseModel, Field, root_validator
from pydantic.networks import EmailStr


class UserSchema(BaseModel):
    name: str = Field(None, min_length=3, max_length=100)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = datetime.now()
    
    class Config:
        pass
    

def user_helper(user) -> dict:
    return{
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "is_active": user["is_active"],
        "is_admin": user["is_admin"],
        "created_at": user["created_at"],
    }
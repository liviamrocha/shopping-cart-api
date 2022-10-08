from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

# Modelo base de um usuário (para cadastro)
class UserSchema(BaseModel):
    name: str = Field(None, min_length=3, max_length=100)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = datetime.now()
    
# Modelo de retorno de um documento de usuário
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "is_active": user["is_active"],
        "is_admin": user["is_admin"],
        "created_at": user["created_at"],
    }
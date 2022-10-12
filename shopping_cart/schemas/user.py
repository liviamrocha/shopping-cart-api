from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

class UserSchema(BaseModel):
    name: str = Field(
        min_length=3, 
        max_length=100,
        description="Nome do usuário"
    )
    email: EmailStr = Field(
        unique=True, 
        index=True,
        description="E-mail do usuário"
    )
    password: str = Field(
        description="Senha do usuário"
    )
    is_active: bool = Field(
        default=True,
        description="Usuário ativo?"
    )
    is_admin: bool = Field(
        default=False,
        description="Usuário administrador?"
    )
    created_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora de criação do usuário"
    )
    updated_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora da última atualização"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "string",
                "email": "string",
                "password": "string"
            }
        }

class AuthenticationResponseSchema(BaseModel):
    name: str = Field(
        min_length=3, 
        max_length=100,
        description="Nome do usuário"
    )
    email: EmailStr = Field(
        unique=True, 
        index=True,
        description="E-mail do usuário"
    )
    is_active: bool = Field(
        default=True,
        description="Usuário ativo?"
    )
    is_admin: bool = Field(
        default=False,
        description="Usuário administrador?"
    )
    created_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora de criação do usuário"
    )
    updated_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora da última atualização"
    )

class PasswordUpdateSchema(BaseModel):
    current_password: str = Field(
        description="Senha atual"
    )
    new_password: str = Field(
        description="Senha nova"
    )

class UserResponse(UserSchema):
    pass
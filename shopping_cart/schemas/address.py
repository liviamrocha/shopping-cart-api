from typing import List
from pydantic import BaseModel, Field
from shopping_cart.schemas.user import UserSchema


# Modelo base de um endereço (para cadastro)
class Address(BaseModel):
    street: str = Field(None, min_length=3, max_length=200)
    number: int 
    city: str = Field(None, min_length=3, max_length=200)
    state: str = Field(None, min_length=3, max_length=200)
    zip_code: int
    is_delivery: bool
    
# Modelo base de criação de uma lista de endereços do usuário
class AddressSchema(BaseModel):
    user: UserSchema
    address: List[Address]

# Modelo de retorno de um documento de endereço com os dados do usuário
def address_helper(address) -> dict:
    user_address = {
        "id": str(address["_id"]),
        "name": address["user"]["name"],
        "email": address["user"]["email"],
        "address": [], 
    }
    for item in address["address"]:
        user_address["address"].append(item)
    return user_address
    
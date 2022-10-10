from typing import List, Optional
from pydantic import BaseModel, Field
from shopping_cart.schemas.user import UserSchema


class AddressSchema(BaseModel):
    city: str = Field(min_length=3, max_length=200)
    state: str = Field(min_length=3, max_length=200)
    zip_code: str
    street: str = Field(min_length=3, max_length=200)
    number: int 
    complement: Optional[str] 
    is_delivery: bool = Field(default=True)

class AdressUpdateSchema(AddressSchema):
    pass


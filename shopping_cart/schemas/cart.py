from math import prod
from pydantic import BaseModel, Field
from shopping_cart.schemas.product import ProductSchema

from shopping_cart.schemas.user import UserSchema


class CartSchema(BaseModel):
    user: UserSchema
    products: ProductSchema = []
    total_quantity: int = 0
    total_price: float = 0
    paid: bool = Field(default=False)
    
    
def cart_helper(cart) -> dict:
    products_list = []
    
    for item in cart["products"]:
        product = {
            "name": item["name"],
            "description": item["description"],
            "price": item["price"],
            "material": item["material"],
            "inmetro": item["inmetro"],
            "code": item["code"],
            "stock": item["stock"],
        }
        products_list.append(product)
        
    return {
        "id": str(cart["_id"]),
        "name": cart.user["name"],
        "email": cart.user["email"],
        "password": cart.user["password"],
        "is_active": cart.user["is_active"],
        "is_admin": cart.user["is_admin"],
        "created_at": cart.user["created_at"],
        "products": products_list,
        "total_quantity": cart["total_quantity"],
        "total_price": cart["total_price"],
        "paid": cart["paid"],
    }
    
        
    
    
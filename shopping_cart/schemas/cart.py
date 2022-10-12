from typing import List
from pydantic import BaseModel, Field
from shopping_cart.schemas.order_item import OrderItemSchema
from shopping_cart.schemas.user import UserSchema
from shopping_cart.schemas.product import ProductSchema



class CartSchema(BaseModel):
    user: UserSchema
    order_items: List[OrderItemSchema] = []
    total_quantity: int = 0
    total_price: float = 0
    paid: bool = Field(default=False)
class CartRequestSchema(BaseModel):
    product_id: int
    quantity: int
class CartResponseSchema(BaseModel):
    order_items: List[OrderItemSchema] = []
    total_quantity: int = 0
    total_price: float = 0
    
def cart_helper(cart) -> dict:
    products_list = []
    
    if len(cart["order_items"]) > 0:
        for item in cart["order_items"]:
            product = {
                "name": item["product"]["name"],
                "description": item["product"]["description"],
                "price": item["product"]["price"],
                "code": item["product"]["code"],
                "quantity": item["quantity"]
                # "name": item["product"]["name"],
                # "description": item["product"]["description"],
                # "price": item["product"]["price"],
                # "material": item["product"]["material"],
                # "inmetro": item["product"]["inmetro"],
                # "code": item["product"]["code"],
                # "stock": item["product"]["stock"],
                # "quantity": item["quantity"],
            }
            products_list.append(product)
        
    return {
        "id": str(cart["_id"]),
        "name": cart["user"]["name"],
        "email": cart["user"]["email"],
        "password": cart["user"]["password"],
        "is_active": cart["user"]["is_active"],
        "is_admin": cart["user"]["is_admin"],
        "created_at": cart["user"]["created_at"],
        "order_items": products_list,
        "total_quantity": cart["total_quantity"],
        "total_price": cart["total_price"],
        "paid": cart["paid"],
    }
    
        
    
    
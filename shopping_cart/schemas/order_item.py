

from typing import Optional
from pydantic import BaseModel
from shopping_cart.schemas.product import ProductSchema


class OrderItemSchema(BaseModel):
    product: Optional[ProductSchema]
    quantity: Optional[int]
    
    
def order_item_helper(order):
    return {
        "id": str(order["_id"]),
        "name": order["order_item"]["product"]["name"],
        "description": order["order_item"]["product"]["description"],
        "price": order["order_item"]["product"]["price"],
        "image": order["order_item"]["product"]["material"],
        "code": order["order_item"]["product"]["code"],
        "quantity": order["order_item"]["quantity"]
    }
    
    #TODO colocar o stock
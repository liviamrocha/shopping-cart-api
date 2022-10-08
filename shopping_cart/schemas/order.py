

from pydantic import BaseModel

from shopping_cart.schemas.address import Address
from shopping_cart.schemas.cart import CartSchema


class OrderSchema(BaseModel):
    cart: CartSchema
    address: Address
    
def order_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "name": order["cart"]["user"]["name"],
        "email": order["cart"]["user"]["email"],
        "password": order["cart"]["user"]["password"],
        "is_active": order["cart"]["user"]["is_active"],
        "is_admin": order["cart"]["user"]["is_admin"],
        "created_at": order["cart"]["user"]["created_at"],
        "order_items": order["cart"]["order_items"],
        "total_quantity": order["cart"]["total_quantity"],
        "total_price": order["cart"]["total_price"],
        "paid": order["cart"]["paid"],
    }
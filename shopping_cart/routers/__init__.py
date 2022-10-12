from fastapi import APIRouter
from . import authentication, index, user, cart, product, order, address



api_router = APIRouter()

api_router.include_router(authentication.router)
api_router.include_router(index.router)
api_router.include_router(user.router)
api_router.include_router(address.router)
api_router.include_router(cart.router)
api_router.include_router(order.router)
api_router.include_router(product.router)

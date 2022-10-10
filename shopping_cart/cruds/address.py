from typing import List, Optional
from pydantic import EmailStr
from shopping_cart.server.database import db
from shopping_cart.schemas.user import UserSchema
from shopping_cart.schemas.address import AddressSchema


async def create_address(user: UserSchema):
    address_document = await db.address_db.insert_one({
        "user": user,
        "address": []
    })
    return address_document


async def add_address(email: EmailStr, address: AddressSchema):
    await db.address_db.find_one_and_update(
        {"user.email": email},
        {"$addToSet": {"address": address}}
    )
    return address
        

async def find_address_by_email(email: EmailStr):
    address_document = await db.address_db.find_one({"user.email": email})
    return address_document
    

async def find_user(email: EmailStr):
    address_document = await db.address_db.find_one({"user.email": email})
    return address_document


async def update_delivered_address(email: EmailStr):
    updated_adresses = await db.address_db.find_one_and_update(
        {'user.email': email, "address.is_delivery": True}, 
        { "$set": { "address.$.is_delivery": False } }
    )
    return updated_adresses


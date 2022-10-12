from typing import List, Optional
from datetime import datetime
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
        
async def find_user(email: EmailStr):
    address_document = await db.address_db.find_one({"user.email": email})
    return address_document

async def find_addresses_by_email(email: EmailStr):
    address_document = await db.address_db.find_one({"user.email": email})
    return address_document

async def find_address_document(email: EmailStr, address_id: str):
    address_document = await db.address_db.find_one(
        {"user.email": email, "address.address_id": address_id},
    )
    return address_document

async def get_delivery_address(email: EmailStr):
    address = await db.address_db.find_one(
        {"user.email": email, 
        "address.is_delivery": True}
    )
    for item in address["address"]:
            if item["is_delivery"] == True:
                delivery_address = item
                break
    return delivery_address

async def delete_address(email, address_id: str):
    deleted_adresses = await db.address_db.update_one(
        {'user.email': email}, 
        {"$pull": {"address": {"address_id": address_id}}}
    )
    return deleted_adresses.modified_count > 0


async def delete_address_document(email):
    document = await db.address_db.delete_one(
        {'user.email': email}
    )
    return document

async def update_delivered_address(email: EmailStr):
    updated_adresses = await db.address_db.find_one_and_update(
        {'user.email': email, "address.is_delivery": True}, 
        { "$set": {"address.$.is_delivery": False, "updated_at": datetime.now()}}
    )
    return updated_adresses

async def update_delivered_automatically(email: EmailStr):
    await db.address_db.find_one_and_update(
        {"user.email": email},
        {"$set" : {"address.0.is_delivery" : True, "updated_at": datetime.now()}}
    )
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr
from shopping_cart.server.database import db
from shopping_cart.schemas.user import UserSchema


async def create_user(user: UserSchema) -> dict:
    new_user = await db.user_db.insert_one(user)
    return new_user


async def get_all_users() -> List[dict]:
    users_cursor = db.user_db.find()
    users = [
        user
        async for user in users_cursor
    ]
    return users


async def get_user_by_email(email: EmailStr) -> Optional[dict]:
    user = await db.user_db.find_one({"email": email})
    return user


async def update_password(email: EmailStr, password_data: dict) -> bool:
    user = await db.user_db.update_one(
        {'email': email},
        {'$set': {'password': password_data['new_password'], "updated_at": datetime.now()}}
    )
    return user.modified_count == 1

async def delete_user(email: EmailStr) -> bool:
    user = await db.user_db.delete_one(
        {'email': email}
    )
    return user.deleted_count > 0
    


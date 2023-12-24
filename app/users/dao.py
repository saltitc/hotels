from sqlalchemy import insert, select
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def create_user(cls, **data):
        user = await cls.add(**data)
        return {"username": user.username, "email": user.email}

    @classmethod
    async def get_user(cls, **filter_by):
        return await cls.find_one_or_none(**filter_by)

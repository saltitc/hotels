from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from app.users.auth import authenticate_user

from app.users.dependencies import get_current_user


class AdminAuthJWTMiddleware(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user_data = await authenticate_user(email, password)

        if user_data:
            request.session.update({
                "access_token": user_data["access_token"],
                "refresh_token": user_data["refresh_token"]
            })

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        user = await get_current_user(token)
        if not user:
            return False

        return True

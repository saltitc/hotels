from httpx import AsyncClient
import pytest
from fastapi import status
from params import REGISTER_DATA

pytest.mark.parametrize()


class TestUsersAPI:
    @pytest.mark.parametrize(
        "username, email, password1, password2, status_code, response_json",
        REGISTER_DATA,
    )
    async def test_register_user(
        self,
        username,
        email,
        password1,
        password2,
        status_code,
        response_json,
        ac: AsyncClient,
    ):
        response = await ac.post(
            "/auth/register",
            json={
                "username": username,
                "email": email,
                "password1": password1,
                "password2": password2,
            },
        )
        assert response.json() == response_json
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "username,password,status_code",
        [
            ("johndoe", "test", 200),
            ("mariavon", "test", 200),
            ("wronguser", "wrong", 401),
        ],
    )
    async def test_login_user(self, username, password, status_code, ac: AsyncClient):
        response = await ac.post(
            "/auth/login", json={"username": username, "password": password}
        )
        assert response.status_code == status_code

    
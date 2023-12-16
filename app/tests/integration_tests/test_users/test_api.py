from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("kot@pes.com", "kot0pes", 409),
        ("abcde", "abcde", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code", [
        ("test@test.com", "test", 200),
        ("user@example.com", "test", 200),
        ("wrong@example.com", "wrong", 401),
        ("abcde", "abcde", 422),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert response.status_code == status_code

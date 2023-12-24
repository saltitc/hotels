import pytest
from app.users.dao import UsersDAO
from app.users.models import Users


class TestUserDAO:
    @pytest.mark.parametrize(
        "id, username, email, password",
        [
            (3, "first_user", "first_user@example.org", "password123"),
            (4, "second_user", "second_user@example.org", "pwd123$#@098def4g$"),
        ],
    )
    async def test_create_user(
        self, id, username: str, email: str, password: str, users_dao=UsersDAO
    ):
        user: Users = await users_dao.create_user(
            username=username,
            email=email,
            password=password,
        )
        assert user.id == id
        assert user.username == username

        user_from_db = await users_dao.get_user(id=user.id, email=user.email)
        assert user_from_db is not None
        assert user_from_db.username == username


    @pytest.mark.parametrize(
        "user_id,username,email,exists",
        [
            (1, "testuser1", "test@test.com", True),
            (2, "fakeuser", "user@example.com", False),
        ],
    )
    async def test_get_user(self, user_id, username, email, exists, users_dao=UsersDAO):
        user: Users = await users_dao.get_user(username=username, email=email)
        if exists:
            assert user.id == user_id
            assert user.username == username
            assert user.email == email
        else:
            assert user is None

    # @pytest.mark.parametrize(
    #     "user_id,email,exists",
    #     [(1, "test@test.com", True), (2, "user@example.com", True), (3, "...", False)],
    # )
    # async def test_find_user_by_id(user_id, email, exists):
    #     user = await UsersDAO.find_by_id(user_id)
    #     if exists:
    #         assert user
    #         assert user.id == user_id
    #         assert user.email == email
    #     else:
    #         assert not user

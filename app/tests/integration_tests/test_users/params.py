from fastapi import status


REGISTER_DATA = [
        (
            "testuser1",
            "user1@test.com",
            "password",
            "password",
            status.HTTP_200_OK,
            {"username": "testuser1", "email": "user1@test.com"},
        ),
        (
            "testuser1",
            "user1@test.com",
            "password",
            "password",
            status.HTTP_409_CONFLICT,
            {"detail": "Пользователь уже существует"},
        ),
        (
            "testuser2",
            "notvalidemail",
            "password",
            "password",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
        (
            "testuser2",
            "user2@test.com",
            "password",
            "passw0rd",
            status.HTTP_400_BAD_REQUEST,
            {"detail": "Пароли не совпадают"},
        ),
    ]


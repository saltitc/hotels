from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoRoomAvailableException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class NotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не найдено"

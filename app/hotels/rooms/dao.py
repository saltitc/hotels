from datetime import date

from app.bookings.dao import BookingDAO
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.schemas import SFreeRooms
from app.dao.base import BaseDAO


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_free_by_hotel(cls, hotel_id: int, date_from: date, date_to: date):
        hotel_rooms = await cls.find_all(hotel_id=hotel_id)
        result = []
        for room in hotel_rooms:
            room = room["Rooms"]
            rooms_left = await BookingDAO.find_free_by_id(room.id, date_from, date_to)
            result.append(
                SFreeRooms(
                    id=room.id,
                    hotel_id=hotel_id,
                    name=room.name,
                    description=room.description,
                    price=room.price,
                    services=room.services,
                    quantity=room.quantity,
                    image_id=room.image_id,
                    total_cost=room.price * (date_to - date_from).days,
                    rooms_left=rooms_left,
                )
            )
        return result

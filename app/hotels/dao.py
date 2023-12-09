from datetime import date
from sqlalchemy import select
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.schemas import SFreeHotels


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_by_location(cls, location: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.location.icontains(location))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_free_by_location(cls, location: str, date_from: date, date_to: date):
        hotels = await cls.find_by_location(location)
        result = []

        for hotel in hotels:
            rooms = await RoomsDAO.find_free_by_hotel(hotel.id, date_from, date_to)
            rooms_left = sum([room.rooms_left for room in rooms])
            result.append(
                SFreeHotels(
                    id=hotel.id,
                    name=hotel.name,
                    location=hotel.location,
                    services=hotel.services,
                    rooms_quantity=hotel.rooms_quantity,
                    image_id=hotel.image_id,
                    rooms_left=rooms_left
                )
            )
        return result
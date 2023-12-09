from datetime import date
from fastapi import APIRouter
from app.exceptions import NotFoundException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SFreeHotels, SHotels
from app.hotels.rooms.router import router as rooms_router


router = APIRouter(prefix="/hotels", tags=["Отели"])
router.include_router(rooms_router)


@router.get("")
async def get_hotels():
    return await HotelsDAO.find_all()


@router.get("/{location}")
async def get_hotels_by_location(
    location: str, date_from: date, date_to: date
) -> list[SFreeHotels]:
    return await HotelsDAO.find_free_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotels:
    hotel = await HotelsDAO.find_one_or_none(id=hotel_id)
    if not hotel:
        raise NotFoundException
    return hotel

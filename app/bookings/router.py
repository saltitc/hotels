from datetime import date
from fastapi import APIRouter, Depends, status
from pydantic import parse_obj_as
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SUserBooking
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomsDAO

# from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import NoRoomAvailableException, NotFoundException

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[SUserBooking]:
    bookings = await BookingDAO.find_all(user_id=user.id)
    result = []
    for booking in bookings:
        booking = booking["Bookings"]
        room = await RoomsDAO.find_by_id(booking.room_id)
        hotel = await HotelsDAO.find_by_id(room.hotel_id)
        result.append(
            SUserBooking(
                id=booking.id,
                room_id=booking.room_id,
                user_id=booking.user_id,
                date_from=booking.date_from,
                date_to=booking.date_to,
                price=booking.price,
                total_cost=booking.total_cost,
                total_days=booking.total_days,
                image_id=hotel.image_id,
                name=hotel.name,
                description=room.description,
                services=hotel.services,
            )
        )
    return result


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise NoRoomAvailableException
    booking_dict = parse_obj_as(SBooking, booking).dict()
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.delete(user, booking_id)
    if not booking:
        raise NotFoundException
    return booking

from datetime import date

from sqlalchemy import and_, between, delete, func, insert, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2033-05-15' AND date_from <= '2033-06-20') OR
            (date_from <= '2033-05-15' AND date_to > '2033-05-15')
        )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == 1,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == 1)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def find_free_by_id(cls, room_id, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms = (
                select(func.count())
                .where(
                    and_(
                        cls.model.room_id == room_id,
                        or_(
                            between(date_to, cls.model.date_from, cls.model.date_to),
                            between(date_from, cls.model.date_from, cls.model.date_to),
                            between(cls.model.date_from, date_from, date_to),
                            between(cls.model.date_to, date_from, date_to),
                        ),
                    )
                )
                .as_scalar()
            )
            get_rooms_left = select(
                func.coalesce(Rooms.quantity - booked_rooms, Rooms.quantity)
            ).where(Rooms.id == room_id)
            result = await session.execute(get_rooms_left)
            return result.scalar()


    @classmethod
    async def delete(cls, current_user, booking_id: int):
        async with async_session_maker() as session:
            delete_query = (
                delete(cls.model)
                .where(
                    and_(
                        cls.model.id == booking_id, cls.model.user_id == current_user.id
                    )
                )
                .returning(cls.model.id)
            )
            delete_booking = await session.execute(delete_query)
            await session.commit()
            return delete_booking.scalar()

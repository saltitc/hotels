from sqladmin.models import ModelView

from app.bookings.models import Bookings


class BookingsAdminView(ModelView, model=Bookings):
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
    column_list = [
        Bookings.id,
        Bookings.user,
        Bookings.room,
        Bookings.date_from,
        Bookings.date_from,
        Bookings.total_days,
        Bookings.total_cost,
        Bookings.user,
        Bookings.room,
    ]
    column_details_list = [
        Bookings.id,
        Bookings.user,
        Bookings.room,
        Bookings.date_from,
        Bookings.date_from,
        Bookings.total_days,
        Bookings.total_cost,
    ]
    form_columns = [
        Bookings.date_from,
        Bookings.date_to,
        Bookings.price,
        Bookings.room,
        Bookings.user,
    ]
    column_searchable_list = [Bookings.user_id, Bookings.room_id]

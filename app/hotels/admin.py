from sqladmin.models import ModelView

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelAdminView(ModelView, model=Hotels):
    name = "Отель"
    name_plural = "Отели"
    column_list = [
        Hotels.id,
        Hotels.name,
        Hotels.location,
        Hotels.services,
        Hotels.rooms,
    ]
    column_details_list = [
        Hotels.name,
        Hotels.location,
        Hotels.services,
        Hotels.rooms,
        Hotels.rooms_quantity,
    ]
    form_columns = [
        Hotels.name,
        Hotels.location,
        Hotels.services,
        Hotels.rooms,
        Hotels.rooms_quantity,
        Hotels.image_id,
    ]
    icon = "fa-solid fa-hotel"


class RoomAdminView(ModelView, model=Rooms):
    name = "Комната"
    name_plural = "Комнаты"
    column_list = [Rooms.id, Rooms.name, Rooms.price, Rooms.hotel]
    column_details_exclude_list = [Rooms.hotel_id, Rooms.image_id, Rooms.id]
    icon = "fa-solid fa-bed"
    form_columns = [
        Rooms.name,
        Rooms.description,
        Rooms.price,
        Rooms.services,
        Rooms.quantity,
        Rooms.image_id,
        Rooms.hotel,
    ]

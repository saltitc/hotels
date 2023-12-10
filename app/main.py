from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from app.config import settings
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.database import engine
from app.users.admin import UserAdminView
from app.bookings.admin import BookingsAdminView
from app.hotels.admin import HotelAdminView, RoomAdminView
from app.middleware import AdminAuthJWTMiddleware


app = FastAPI()

static_files = StaticFiles(directory="app/static")

app.mount("/static", static_files, "static")
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_images)

admin = Admin(app, engine, authentication_backend=AdminAuthJWTMiddleware(None))

views = [UserAdminView, BookingsAdminView, HotelAdminView, RoomAdminView]

for view in views:
    admin.add_view(view)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

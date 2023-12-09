from pydantic import BaseModel
from typing import List


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    class Config:
        orm_mode = True


class SFreeHotels(SHotels):
    rooms_left: int

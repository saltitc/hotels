from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False, server_default="FALSE")
    is_staff = Column(Boolean, default=False, server_default="FALSE")
    is_superuser = Column(Boolean, default=False, server_default="FALSE")

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"Пользователь #{self.id}: {self.username}"

    def __repr__(self):
        return f"<User {self.username}>"


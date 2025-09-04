from database.models.base import AbstractModel
from sqlalchemy import Column, String


class User(AbstractModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)


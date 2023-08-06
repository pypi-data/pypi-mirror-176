from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

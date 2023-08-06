from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from marshmallow import fields
from marshmallow import Schema

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(100), nullable=False)


class UserSchema(Schema):

    model_class = User

    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()

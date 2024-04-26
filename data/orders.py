import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import orm
import datetime
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'order'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_order = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teg = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    if_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    is_paid = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=False)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=datetime.datetime.now)
    user = orm.relationship('User')


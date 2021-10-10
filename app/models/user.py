# -*- coding: utf-8 -*-
from app.db import db
from app.models.user_has_roles import user_has_roles
from sqlalchemy import or_
import datetime


class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow) #se modifico para que se guarde la fecha en la bd
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    roles = db.relationship(
        "Role",
        secondary="user_has_roles",
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def __repr__(self):
        return "<User %r>" % self.username

    def __init__(
        self,
        email: str = None,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        active: int = None,
    ):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.active = active

    @classmethod
    def find_by_email_and_pass(cls, email, password):
        return User.query.filter(User.email==email and User.password==password).first()

    @classmethod
    def check_existing_email_or_username(cls, email, username):
        return User.query.filter(or_(User.username==username, User.email==email)).first()

    @classmethod
    def insert_user(cls, new_user):
        db.session.add(new_user)
        db.session.commit()   

    @classmethod
    def find_all_users(cls):
        return User.query.all()

# class User(object):
#     @classmethod
#     def all(cls, conn):
#         sql = "SELECT * FROM users"
#         cursor = conn.cursor()
#         cursor.execute(sql)

#         return cursor.fetchall()

#     @classmethod
#     def create(cls, conn, data):
#         sql = """
#             INSERT INTO users (email, password, first_name, last_name)
#             VALUES (%s, %s, %s, %s)
#         """

#         cursor = conn.cursor()
#         cursor.execute(sql, list(data.values()))
#         conn.commit()

#         return True

#     @classmethod
#     def find_by_email_and_pass(cls, conn, email, password):
#         sql = """
#             SELECT * FROM users AS u
#             WHERE u.email = %s AND u.password = %s
#         """

#         cursor = conn.cursor()
#         cursor.execute(sql, (email, password))

# return cursor.fetchone()

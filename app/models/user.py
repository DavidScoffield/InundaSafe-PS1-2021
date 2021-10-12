# -*- coding: utf-8 -*-
from sqlalchemy import or_
import datetime
from app.db import db
from app.helpers.bcrypt import check_password, generate_password_hash
from app.models.user_has_roles import user_has_roles


class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )  # se modifico para que se guarde la fecha en la bd
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
        """
        - Busca en la base de datos a un usuario que tenga el mismo mail
        - Si lo encuentra cumprueba que el que recupera tenga la misma contraseña que la que llega como parametro, y devuelve al usuario encontrado
        - Caso contrario retorna None
        """

        user_find = User.query.filter(User.email == email).first()
        return (
            user_find if (user_find and user_find.verify_password(password)) else None
        )

    @classmethod
    def check_existing_email_or_username(cls, email, username):
        return User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()

    @classmethod
    def insert_user(cls, new_user):
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def find_all_users(cls):
        return User.query.all()

    @property
    def password(self):
        "Creacion de excepcion en caso de que se quiera hacer el get de password"
        raise AttributeError("Contraseña no legible")

    @password.setter
    def password(self, password):
        "Setter para la password, y al momento de realizarla, crear la contraseña hasheada y almacenar esta en vez del string"
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        "Comprueba que la contraseña pasada sea la misma que la que tiene almacenada hasheada"
        return check_password(self.password_hash, password)

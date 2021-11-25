# -*- coding: utf-8 -*-
from app.db import db


class UserWaiting(db.Model):
    """Modelo para el manejo de la tabla User Waiting de la base de datos"""

    __tablename__ = "users_waiting"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(150), nullable=False, unique=True
    )
    suggested_username = db.Column(
        db.String(50), nullable=False, unique=True
    )
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<UserWaiting %r>" % self.email

    def __init__(
        self,
        email: str = None,
        suggested_username: str = None,
        first_name: str = None,
        last_name: str = None,
    ):
        """Constructor del modelo"""
        self.email = email
        self.suggested_username = suggested_username
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def new(
        cls,
        email,
        suggested_username,
        password,
        first_name,
        last_name,
    ):
        """Insertar un nuevo usuario en la base de datos con los datos pasados por parametro"""
        new_user = UserWaiting(
            email,
            suggested_username,
            password,
            first_name,
            last_name,
        )
        db.session.add(new_user)
        db.session.commit()

    def delete(self):
        "Borra un usuario en espera"

        db.session.delete(self)
        db.session.commit()

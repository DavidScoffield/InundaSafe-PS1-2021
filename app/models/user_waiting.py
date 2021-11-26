# -*- coding: utf-8 -*-
from app.db import db
from app.helpers.config import actual_config


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

    @classmethod
    def check_existing_email(
        cls,
        email: str = None,
    ):
        """Comprobar si algun usuario con determinado email"""
        return cls.query.filter(
            cls.email == email,
        ).first()

    @classmethod
    def search_paginate(
        cls,
        page_number: int = 1,
        email: str = "",
    ):
        """
        Retorna una lista con todos los usuarios, teniendo en cuenta los filtros
        pasados por parametro, en caso que estos sean vacio retorna todos los usuarios.
        Pagina el resultado
        """
        ordered_users = cls.search(email=email)
        paginated_users = cls.paginate(
            ordered_users, page_number
        )
        return paginated_users

    @classmethod
    def search(
        cls,
        email: str = "",
    ):
        """
        Retorna una lista con todos los usuarios, teniendo en cuenta los filtros
        pasados por parametro, en caso que estos sean vacio retorna todos los usuarios.
        """

        ac = actual_config()
        order = ac.order_by
        return cls.query.filter(
            cls.email.contains(email)
        ).order_by(eval(f"UserWaiting.email.{order}()"))

    @classmethod
    def paginate(
        cls,
        users,
        page_number: int = 1,
    ):
        "Retorna la lista de usuarios pasados por parametro paginados"
        ac = actual_config()
        elements_quantity = ac.elements_quantity
        return users.paginate(
            max_per_page=elements_quantity,
            per_page=elements_quantity,
            page=page_number,
            error_out=False,
        )

    @classmethod
    def find_user_by_id(cls, user_id):
        """Buscar usuario en la base de datos por id"""
        return cls.query.filter(cls.id == user_id).first()

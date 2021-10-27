# -*- coding: utf-8 -*-
from sqlalchemy import or_
import datetime
from app.db import db
from app.helpers.bcrypt import (
    check_password,
    generate_password_hash,
)
from app.models.user_has_roles import user_has_roles
from app.models.role import Role
from app.helpers.config import actual_config
from app.helpers.from_intState_to_stringState import active_dic

class User(db.Model):
    """Modelo para el manejo de la tabla User de la base de datos"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(150), nullable=False, unique=True
    )
    username = db.Column(
        db.String(50), nullable=False, unique=True
    )
    password_hash = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )  # se modifico para que se guarde la fecha en la bd
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )
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
        is_deleted: int = 0,
    ):
        """Constructor del modelo"""
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.active = active
        self.is_deleted = is_deleted

    def get_attributes(self):
        "Retorna un diccionario con los atributos del usuario"
        
        attributes = vars(self)
        del attributes["_sa_instance_state"]

        #Convierte de 1 a 'activo' o de 0 a 'bloqueado' para el WTF
        attributes["active"] = active_dic(attributes["active"])

        #Roles por defecto que tiene el user, los agrego para que matcheen con WTF
        for rol in attributes["roles"]:
            attributes[rol.name] = True

        return attributes


    @classmethod
    def find_by_email_and_pass(cls, email, password):
        """
        - Busca en la base de datos a un usuario que tenga el mismo mail
        - Si lo encuentra cumprueba que el que recupera tenga la misma contraseña
        que la que llega como parametro, y devuelve al usuario encontrado
        - Caso contrario retorna None
        """

        user_find = User.query.filter(
            User.email == email
        ).first()
        return (
            user_find
            if (
                user_find
                and user_find.verify_password(password)
            )
            else None
        )

    @classmethod
    def update_state(cls, user_id, new_state):
        """Actualizar estado del usuario"""
        user = User.query.filter(User.id == user_id).first()
        user.active = new_state
        db.session.commit()

    @classmethod
    def find_user_by_id(cls, user_id):
        """Buscar usuario en la base de datos por id"""
        return User.query.filter(User.id == user_id).first()

    @classmethod
    def find_user_by_id_not_deleted(cls, user_id):
        """Buscar usuario en la base de datos por id"""
        return (
            User.query.filter(User.id == user_id)
            .filter(User.is_deleted == 0)
            .first()
        )

    @classmethod
    def check_existing_email_or_username(
        cls, email, username
    ):
        """Comprobar si algun usuario con determinado email o nombre de usuario"""
        return User.query.filter(
            or_(
                User.username == username,
                User.email == email,
            )
        ).first()

    @classmethod
    def check_existing_email_with_different_id(
        cls, email, id_user
    ):
        """Comprobar si existe algun usuario con determinado email
        y que no sea el del usuario con id = id_user"""
        return (
            User.query.filter(User.email == email)
            .filter(User.id != id_user)
            .first()
        )

    @classmethod
    def update_user(cls, user_id, data, selectedRoles, update_password):
        """Actualizar usuario en la base de datos con los datos pasados por parametros"""
        user = User.find_user_by_id(user_id)
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        if(update_password):
            user.password = data["password"]
        if (
            data["active"] == "activo"
        ):  # depende cual sea el estado pongo un int 1 o 0 para q quede acorde con bd
            user.active = 1
        else:
            user.active = 0
        db.session.commit()
        roles = Role.find_roles_from_strings(selectedRoles)

        Role.delete_rol(user.roles, user)
        Role.insert_rol(roles, user)

    @classmethod
    def update_profile(
        cls, user, data, selectedRoles, isAdmin
    ):
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.password = data["password"]
        db.session.commit()

        if isAdmin:
            roles = Role.find_roles_from_strings(
                selectedRoles
            )

            Role.delete_rol(user.roles, user)
            Role.insert_rol(roles, user)

    @classmethod
    def insert_user(
        cls,
        email,
        username,
        password,
        first_name,
        last_name,
        state,
        selectedRoles,
    ):
        """Insertar un nuevo usuario en la base de datos con los datos pasados por parametro"""
        new_user = User(
            email,
            username,
            password,
            first_name,
            last_name,
            state,
        )
        db.session.add(new_user)
        db.session.commit()

        roles = Role.find_roles_from_strings(
            selectedRoles
        )  # lista con los roles que va a tener el nuevo usuario
        Role.insert_rol(
            roles, new_user
        )  # inserto los roles en la tabla user_has_roles

    @classmethod
    def find_all_users(cls):
        """Buscar todos los usuarios de la base de datos"""
        return User.query.all()

    @classmethod
    def search_paginate(
        cls,
        page_number: int = 1,
        name: str = "",
        active: int = 1,
        dont_use_active: bool = True,
    ):
        """
        Retorna una lista con todos los usuarios, teniendo en cuenta los filtros
        pasados por parametro, en caso que estos sean vacio retorna todos los usuarios.
        Pagina el resultado
        """
        ordered_users = User.search(
            name=name,
            active=active,
            dont_use_active=dont_use_active,
        )
        paginated_users = User.paginate(
            ordered_users, page_number
        )
        return paginated_users

    @classmethod
    def search(
        cls,
        username: str = "",
        active: int = 1,
        dont_use_active: bool = True,
    ):
        """
        Retorna una lista con todos los usuarios, teniendo en cuenta los filtros
        pasados por parametro, en caso que estos sean vacio retorna todos los usuarios.
        """

        ac = actual_config()
        order = ac.order_by
        return (
            User.query.filter(User.is_deleted == 0)
            .filter(User.username.contains(username))
            .filter(
                or_(User.active == active, dont_use_active)
            )
            .order_by(eval(f"User.first_name.{order}()"))
        )

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
    def exclude_user(cls, users, user_id):
        """Filtrar de la lista de usuarios aquel con id = user_id"""
        return users.filter(User.id != user_id)

    # Baja logica
    @classmethod
    def delete_user(cls, user_id):
        """Eliminar de la base de datos a un usuario en base al id"""
        user = User.query.filter(User.id == user_id).first()
        user.is_deleted = 1
        db.session.commit()

    @property
    def password(self):
        "Creacion de excepcion en caso de que se quiera hacer el get de password"
        raise AttributeError("Contraseña no legible")

    @password.setter
    def password(self, password):
        """
        Setter para la password, y al momento de realizarla,
        crear la contraseña hasheada y almacenar esta en vez del string
        """

        self.password_hash = generate_password_hash(
            password
        )

    def verify_password(self, password: str):
        "Comprueba que la contraseña pasada sea la misma que la que tiene almacenada hasheada"
        return check_password(self.password_hash, password)

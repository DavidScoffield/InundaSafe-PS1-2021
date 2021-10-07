# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


user_has_roles = db.Table(
    "user_has_roles",
    db.Column("role_id", db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "user_id",
        db.ForeignKey("users.id"),
        primary_key=True,
    ),
)


role_has_permissions = db.Table(
    "role_has_permissions",
    db.Column("role_id", db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permission_id",
        db.ForeignKey("permissions.id"),
        primary_key=True,
    ),
)


class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
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


class Role(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    permissions = db.relationship(
        "Permission",
        secondary="role_has_permissions",
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )

    def __repr__(self):
        return "<Role %r>" % self.name

    def __init__(self, name: str = None):
        self.name = name


class Permission(db.Model):

    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Permission %r>" % self.name

    def __init__(self, name: str = None):
        self.name = name


class MeetingPoint(db.Model):

    __tablename__ = "meeting_point"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    coor_X = db.Column(db.String(100))
    coor_Y = db.Column(db.String(100))
    state = db.Column(db.String(100))
    telephone = db.Column(db.String(50))
    email = db.Column(db.String(150))

    def __repr__(self):
        return "<MeetingPoint %r>" % self.name

    def __init__(
        self,
        name: str = None,
        address: str = None,
        coor_X: str = None,
        coor_Y: str = None,
        state: str = None,
        telephone: str = None,
        email: str = None,
    ):
        self.name = name
        self.address = address
        self.coor_X = coor_X
        self.coor_Y = coor_Y
        self.state = state
        self.telephone = telephone
        self.email = email


class Color(db.Model):

    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    color_1 = db.Column(db.String(15), nullable=False)
    color_2 = db.Column(db.String(15), nullable=False)
    color_3 = db.Column(db.String(15), nullable=False)
    color_4 = db.Column(db.String(15), nullable=False)
    color_5 = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return "<Color %r>" % self.id

    def __init__(
        self,
        color_1: str = None,
        color_2: str = None,
        color_3: str = None,
        color_4: str = None,
        color_5: str = None,
    ):
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.color_5 = color_5


class Configuration(db.Model):

    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    elements_quantity = db.Column(db.Integer, nullable=False, default=50)
    order_by = db.Column(db.String(25), nullable=False, default="asc")
    colors_id_public = db.Column(
        db.Integer, db.ForeignKey("colors.id"), nullable=False, default="asc"
    )
    colors_public = db.relationship("Color", foreign_keys=[colors_id_public])
    colors_id_private = db.Column(
        db.Integer, db.ForeignKey("colors.id"), nullable=False, default="asc"
    )
    colors_private = db.relationship("Color", foreign_keys=[colors_id_private])

    def __repr__(self):
        return "<Configuration %r>" % self.id

    def __init__(
        self,
        elements_quantity: int = None,
        order_by: str = None,
        colors_id_public: int = None,
        colors_id_private: int = None,
    ):
        self.elements_quantity = elements_quantity
        self.order_by = order_by
        self.colors_id_public = colors_id_public
        self.colors_id_private = colors_id_private

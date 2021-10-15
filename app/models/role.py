# -*- coding: utf-8 -*-
from app.db import db
from app.models.role_has_permissions import role_has_permissions


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

    @classmethod
    def find_roles_from_strings(cls, roles):
        return Role.query.filter(Role.name.in_(roles)).all()

    @classmethod
    def insert_rol(cls, roles, new_user):
        for rol in roles:
            new_user.roles.append(rol) 
        db.session.commit() 

    @classmethod
    def delete_rol(cls, roles, new_user):
        for rol in roles:
            new_user.roles.clear(rol) 
        db.session.commit()  
    
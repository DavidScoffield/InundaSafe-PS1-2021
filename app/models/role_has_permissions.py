# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


role_has_permissions = db.Table(
    "role_has_permissions",
    db.Column("role_id", db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permission_id",
        db.ForeignKey("permissions.id"),
        primary_key=True,
    ),
)

# class RoleHasPermissions(db.Model):

#     __tablename__ = "role_has_permissions"
#     role_id = db.Column(db.Integer, primary_key=True)
#     permission_id = db.Column(db.Integer, primary_key=True)

#     def __repr__(self):
#         return '<Permission %r>' % self.name

#     def __init__(self, role_id: int = None, permission_id: int = None):
#         self.role_id = role_id
#         self.permission_id = permission_id

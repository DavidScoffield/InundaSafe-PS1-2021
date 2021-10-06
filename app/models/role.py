# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

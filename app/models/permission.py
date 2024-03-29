# -*- coding: utf-8 -*-
from app.db import db


class Permission(db.Model):
    """Modelo para el manejo de la tabla Permission de la base de datos"""

    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Permission %r>" % self.name

    def __init__(self, name: str = None):
        """Constructor del modelo"""
        self.name = name

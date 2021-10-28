# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship
from app.db import db


class FloodZones(db.Model):
    """Modelo para el manejo de la tabla FloodZones de la base de datos"""

    __tablename__ = "flood_zones"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(15), nullable=False)
    coordinates = relationship("Coordinate")

    def __repr__(self):
        return "<FloodZones %r>" % self.name

    def __init__(
        self,
        name: str = None,
        state: str = None,
        color: str = None,
        coordinates: list = None,
    ):
        """Constructor del modelo"""
        self.name = name
        self.state = state
        self.color = color
        self.coordinates = coordinates

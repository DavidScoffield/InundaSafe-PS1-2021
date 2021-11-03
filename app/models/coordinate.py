# -*- coding: utf-8 -*-
from app.db import db
from sqlalchemy import Index


class Coordinate(db.Model):
    """Modelo para el manejo de la tabla Coordinate de la base de datos"""

    __tablename__ = "Coordinate"
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    evacuation_route_id = db.Column(
        db.Integer,
        db.ForeignKey("evacuation_route.id"),
        nullable=True,
    )

    __table_args__ = (
        Index(
            "latitude_longitude", "latitude", "longitude"
        ),
    )

    def __repr__(self):
        return f"[{self.latitude}, {self.longitude}]"

    def __init__(
        self,
        latitude: str = None,
        longitude: str = None,
    ):
        """Constructor del modelo"""
        self.latitude = latitude
        self.longitude = longitude

# -*- coding: utf-8 -*-
from app.db import db
from sqlalchemy import Index


class Coordinate(db.Model):
    """Modelo para el manejo de la tabla Coordinate de la base de datos"""

    __tablename__ = "coordinate"
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    flood_zone_id = db.Column(
        db.Integer,
        db.ForeignKey("flood_zones.id", ondelete="CASCADE"),
        nullable=True,
    )
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

    @classmethod
    def new(
        cls,
        latitude: str = None,
        longitude: str = None,
    ):
        """
        Recibe los parámetros para crear la Coordenada.
        La guarda en la base de datos.
        Devuelve la coordenada creada
        """

        coordinate = Coordinate(latitude, longitude)
        db.session.add(coordinate)
        db.session.commit()
        return coordinate

    def as_array(self):
        return [self.latitude, self.longitude]

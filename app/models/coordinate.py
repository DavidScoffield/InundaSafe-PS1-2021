# -*- coding: utf-8 -*-
from app.db import db
from sqlalchemy import Index, func
from sqlalchemy.ext.hybrid import hybrid_method
import math

class Coordinate(db.Model):
    """Modelo para el manejo de la tabla Coordinate de la base de datos"""

    __tablename__ = "coordinate"
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    flood_zone_id = db.Column(
        db.Integer,
        db.ForeignKey("flood_zones.id", ondelete="CASCADE"),
        nullable=True,
    )
    evacuation_route_id = db.Column(
        db.Integer,
        db.ForeignKey("evacuation_route.id", ondelete="CASCADE"),
        nullable=True,
    )
    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaint.id", ondelete="CASCADE"),
        nullable=True,
    )
    meeting_point_id = db.Column(
        db.Integer,
        db.ForeignKey("meeting_point.id", ondelete="CASCADE"),
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
        latitude = None,
        longitude = None,
    ):
        """Constructor del modelo"""
        self.latitude = float(latitude)
        self.longitude = float(longitude)

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

    @hybrid_method
    def distance_between(self, lat2, long2):
        pass

    @distance_between.expression
    def distance_between(self, y2, x1):
        "Función que retorna la distancia entre la coordenada y otro punto"

        y1 = self.latitude
        x2 = self.longitude

        return func.pow((((x2 - x1 ) * (x2 - x1 )) + ((y2 - y1) * (y2 - y1))), 0.5)
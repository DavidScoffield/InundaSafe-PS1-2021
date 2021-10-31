# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship
from app.db import db
from app.models.coordinate import Coordinate


class FloodZones(db.Model):
    """Modelo para el manejo de la tabla FloodZones de la base de datos"""

    __tablename__ = "flood_zones"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    state = db.Column(
        db.String(100), default="publicated", nullable=True
    )
    color = db.Column(db.String(15), nullable=True)
    coordinates = relationship(
        "Coordinate", cascade="all,delete-orphan"
    )

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
        self.add_coordinates(coordinates)

    @classmethod
    def new(
        cls,
        name: str = None,
        state: str = None,
        color: str = None,
        coordinates: list = None,
    ):
        """
        Recibe los parámetros para crear una zona inundable.
        La guarda en la base de datos
        """
        flood_zone = FloodZones(
            name, state, color, coordinates
        )
        db.session.add(flood_zone)
        db.session.commit()
        return flood_zone

    @classmethod
    def find_by_name(cls, name: str):
        """Busca una zona inundable por nombre"""
        return FloodZones.query.filter(
            FloodZones.name == name
        ).first()

    def update(
        self,
        state: str = None,
        color: str = None,
        coordinates: list = None,
    ):
        self.state = (
            state if state is not None else self.state
        )
        self.color = (
            color if color is not None else self.color
        )
        if coordinates is not None:
            self.delete_coordinates()
            self.add_coordinates(coordinates)

        db.session.commit()

    def delete_coordinates(self):
        # TODO: SOLUCIONAR ELIMINACION
        for coordinate in self.coordinates:
            self.coordinates.delete(coordinate)

    def add_coordinates(self, list_coordinates: list):
        for coordinate in list_coordinates:
            c = Coordinate.new(
                latitude=str(coordinate[0]),
                longitude=str(coordinate[1]),
            )
            self.coordinates.append(c)

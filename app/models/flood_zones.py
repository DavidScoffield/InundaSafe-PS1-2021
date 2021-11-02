# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship
from app.db import db
from app.models.coordinate import Coordinate
from app.helpers.uuid import generate_unique_uuid


class FloodZones(db.Model):
    """Modelo para el manejo de la tabla FloodZones de la base de datos"""

    __tablename__ = "flood_zones"
    id = db.Column(db.Integer, primary_key=True)
    cipher = db.Column(db.String(255), nullable=False)
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
        """Constructor del modelo FloodZones"""
        self.name = name
        self.state = state
        self.color = color
        self.cipher = generate_unique_uuid()
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
        """
        Metodo para actializar una zona inundable.
        Actualizaro solo aquellos parametros que sean pasados en la invocacion
        """
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
        """
        Elimina todas sus coordenadas
        """
        self.coordinates.clear()
        db.session.commit()

    def add_coordinates(self, list_coordinates: list):
        """
        Agrega las coordenadas pasados por parametro
        """
        for coordinate in list_coordinates:
            c = Coordinate.new(
                latitude=str(coordinate[0]),
                longitude=str(coordinate[1]),
            )
            self.coordinates.append(c)

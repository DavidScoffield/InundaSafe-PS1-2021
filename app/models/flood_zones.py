# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship
from werkzeug.datastructures import cache_property
from app.db import db
from app.helpers.config import actual_config
from app.models.coordinate import Coordinate
from app.helpers.uuid import generate_unique_uuid
from app.helpers.validate_coordinates import (
    coordinates_encode,
)
from app.helpers.logger import logger_info


class FloodZones(db.Model):
    """Modelo para el manejo de la tabla FloodZones de la base de datos"""

    __tablename__ = "flood_zones"
    id = db.Column(db.Integer, primary_key=True)
    cipher = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    state = db.Column(
        db.String(100), default="publicated", nullable=True
    )
    color = db.Column(
        db.String(15), default="#78849D", nullable=True
    )
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

    def get_attributes(self):
        "Retorna un diccionario con los atributos de la zona inundable"
        attributes = vars(self)
        attributes["coordinates"] = coordinates_encode(
            self.coordinates
        )
        del attributes["_sa_instance_state"]

        return attributes

    @classmethod
    def all(cls, page: int = None, per_page: int = None):
        return cls.query.paginate(
            per_page=per_page,
            page=page,
            error_out=True,
        )

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
    def find_by_id(cls, id):
        "Retorna la zona inundable correspondiente al id recibido por parámetro"

        return FloodZones.query.get(id)

    @classmethod
    def find_by_name(cls, name: str):
        """Busca una zona inundable por nombre"""
        return FloodZones.query.filter(
            FloodZones.name == name
        ).first()

    @classmethod
    def exist_name(
        cls,
        name_to_find: str = None,
    ):
        """
        Verifica si el nombre de zona inundable pasado ya esta en uso
        """
        return (
            FloodZones.query.filter(
                FloodZones.name.ilike(name_to_find),
            ).first()
            is not None
        )

    @classmethod
    def search(
        cls,
        page_number: int = 1,
        name: str = "",
        state: str = "",
    ):
        """
        Retorna una lista con todas las zones inundables, teniendo
        en cuenta los filtros pasados por parametro, en caso que estos
        sean vacio retorna todas las zonas inundables.
        Retorna el resultado paginado
        """

        ac = actual_config()
        order = ac.order_by
        ordered_flood_zones = (
            FloodZones.query.filter(
                FloodZones.name.contains(name)
            )
            .filter(FloodZones.state.startswith(state))
            .order_by(eval(f"FloodZones.name.{order}()"))
        )
        paginated_flood_zones = FloodZones.paginate(
            ordered_flood_zones, page_number
        )
        return paginated_flood_zones

    @classmethod
    def paginate(
        cls,
        flood_zones,
        page_number: int = 1,
    ):
        "Retorna la lista de meeting points pasados por parametro paginados"
        ac = actual_config()
        elements_quantity = ac.elements_quantity
        paginated_flood_zones = flood_zones.paginate(
            max_per_page=elements_quantity,
            per_page=elements_quantity,
            page=page_number,
            error_out=False,
        )
        return paginated_flood_zones

    def update(
        self,
        name: str = None,
        state: str = None,
        color: str = None,
        coordinates: list = None,
    ):
        """
        Metodo para actializar una zona inundable.
        Actualizaro solo aquellos parametros que sean pasados en la invocacion
        """
        self.name = name if name is not None else self.name
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

    def delete(self):
        "Borra la zona de inundacion"

        db.session.delete(self)
        db.session.commit()

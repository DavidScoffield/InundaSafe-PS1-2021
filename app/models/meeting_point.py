# -*- coding: utf-8 -*-
from app.db import db
from app.helpers.config import actual_config
from sqlalchemy.orm import relationship
from app.models.coordinate import Coordinate


class MeetingPoint(db.Model):
    """Modelo para el manejo de la tabla MeetingPoint de la base de datos"""

    __tablename__ = "meeting_point"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    coordinate = relationship(
        "Coordinate",
        uselist=False,
        cascade="all,delete-orphan",
    )
    state = db.Column(db.String(100))
    telephone = db.Column(db.String(50))
    email = db.Column(db.String(150))

    def __repr__(self):
        return "<MeetingPoint %r>" % self.name

    def __init__(
        self,
        name: str = None,
        address: str = None,
        coordinate: list = None,
        state: str = None,
        telephone: str = None,
        email: str = None,
    ):
        """Constructor del modelo"""
        self.name = name
        self.address = address
        self.coordinate = Coordinate(
            coordinate[0], coordinate[1]
        )
        self.state = state
        self.telephone = telephone
        self.email = email

    @classmethod
    def all(cls, page: int = None, per_page: int = None):
        """
        Devuelve los puntos de encuentro publicacos, paginados en base a los
        parametros pasados, en caso de que se pasen
        """

        ac = actual_config()
        order = ac.order_by

        return (
            cls.query.filter(cls.state == "publicated")
            .order_by(eval(f"MeetingPoint.name.{order}()"))
            .paginate(
                per_page=per_page,
                page=page,
                error_out=True,
            )
        )

    @classmethod
    def new(cls, **args):
        "Recibe los parámetros para crear el meeting point y lo guarda en la base de datos"

        meeting_point = MeetingPoint(**args)
        db.session.add(meeting_point)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        "Retorna el meeting point correspondiente al id recibido por parámetro"

        return MeetingPoint.query.get(id)

    def get_attributes(self, keep_instance_state=True):
        "Retorna un diccionario con los atributos del meeting point"

        attributes = vars(self)
        attributes["coordinate"] = self.coordinate
        if not keep_instance_state:
            del attributes["_sa_instance_state"]

        return attributes

    @classmethod
    def search(
        cls,
        page_number: int = 1,
        name: str = "",
        state: str = "",
    ):
        """
        Retorna una lista con todos los meeting points, teniendo en cuenta los filtros pasados
        por parametro, en caso que estos sean vacio retorna todos los meeting points.
        Retorna el resultado paginado
        """

        ac = actual_config()
        order = ac.order_by
        ordered_meeting_points = (
            MeetingPoint.query.filter(
                MeetingPoint.name.contains(name)
            )
            .filter(MeetingPoint.state.startswith(state))
            .order_by(eval(f"MeetingPoint.name.{order}()"))
        )
        paginated_meeting_points = MeetingPoint.paginate(
            ordered_meeting_points, page_number
        )
        return paginated_meeting_points

    @classmethod
    def paginate(
        cls,
        meeting_points,
        page_number: int = 1,
    ):
        "Retorna la lista de meeting points pasados por parametro paginados"
        ac = actual_config()
        elements_quantity = ac.elements_quantity
        paginated_meeting_points = meeting_points.paginate(
            max_per_page=elements_quantity,
            per_page=elements_quantity,
            page=page_number,
            error_out=False,
        )
        return paginated_meeting_points

    @classmethod
    def exists_address(cls, address):
        "Verifica si existe un punto de encuentro con la dirección recibida por parámetro"

        return (
            MeetingPoint.query.filter(
                MeetingPoint.address.ilike(address)
            ).first()
            is not None
        )

    def delete(self):
        "Borra un punto de encuentro y su coordenada asociada"

        db.session.delete(self)
        db.session.commit()

    def update(self, **args):
        "Actualiza los datos del meeting point con los recibidos por parámetro"

        for attribute, value in args.items():
            if attribute == "coordinate":
                db.session.delete(self.coordinate)
                self.coordinate = Coordinate(
                    value[0], value[1]
                )
            else:
                setattr(self, attribute, value)

        db.session.commit()

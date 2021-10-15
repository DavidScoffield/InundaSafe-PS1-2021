# -*- coding: utf-8 -*-
from app.db import db
from app.helpers.config import actual_config

class MeetingPoint(db.Model):

    __tablename__ = "meeting_point"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    coor_X = db.Column(db.String(100))
    coor_Y = db.Column(db.String(100))
    state = db.Column(db.String(100))
    telephone = db.Column(db.String(50))
    email = db.Column(db.String(150))

    def __repr__(self):
        return "<MeetingPoint %r>" % self.name

    def __init__(
        self,
        name: str = None,
        address: str = None,
        coor_X: str = None,
        coor_Y: str = None,
        state: str = None,
        telephone: str = None,
        email: str = None,
    ):
        self.name = name
        self.address = address
        self.coor_X = coor_X
        self.coor_Y = coor_Y
        self.state = state
        self.telephone = telephone
        self.email = email
    
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

    def get_attributes(self):
        "Retorna un diccionario con los atributos del meeting point"

        attributes = vars(self)
        del attributes["_sa_instance_state"]
        del attributes["id"]

        return attributes

    @classmethod
    def paginate(cls, page_number):
        "Retorna una lista con todos los meeting points, teniendo en cuenta el paginado"

        elements_quantity = actual_config().elements_quantity
        order = actual_config().order_by
        ordered_meeting_points = MeetingPoint.query.order_by(eval(f"MeetingPoint.name.{order}()"))
        paginated_meeting_points = ordered_meeting_points.paginate(max_per_page = elements_quantity, per_page = elements_quantity, page=page_number, error_out = True)

        return paginated_meeting_points

    @classmethod
    def exists_address(cls, address):
        "Verifica si existe un punto de encuentro con la dirección recibida por parámetro"
        
        return MeetingPoint.query.filter(MeetingPoint.address.ilike(address)).first() is not None

    @classmethod
    def delete(cls, id):
        "Borra un punto de encuentro"

        meeting_point = MeetingPoint.query.filter_by(id = id).first()

        db.session.delete(meeting_point)
        db.session.commit()

    def update(self, **args):
        "Actualiza los datos del meeting point con los recibidos por parámetro"
        
        for attribute, value in args.items():
            setattr(self, attribute, value)
            
        db.session.commit()
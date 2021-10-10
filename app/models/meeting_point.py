# -*- coding: utf-8 -*-
from app.db import db


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
    def meeting_point_new(cls, **args):
        "Recibe los parámetros del formulario, crea el meeting point y lo guarda en la base de datos"

        meeting_point = MeetingPoint(**args)
        db.session.add(meeting_point)
        db.session.commit()
from app.db import db
from app.helpers.config import actual_config
from sqlalchemy.orm import relationship
from app.models.coordinate import Coordinate
import datetime

class Complaint(db.Model):
    """Modelo para las denuncias"""

    __tablename__ = "complaint"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(100))
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )
    closed_at = db.Column(
        db.DateTime
    )
    description = db.Column(db.String(500))
    state = db.Column(db.String(100))
    creator_first_name = db.Column(db.String(100))
    creator_last_name = db.Column(db.String(100))
    creator_telephone = db.Column(db.String(50))
    creator_email = db.Column(db.String(150))
    assigned_to = db.Column(
        db.Integer, 
        db.ForeignKey("users.id"))
    coordinate = relationship("Coordinate", uselist=False)    #,cascade="all,delete", cascade="all,delete-orphan") ?. uselist=False es para one to one
    follow_ups = relationship("ComplaintFollowUp")

    def __repr__(self):
        return "<Complaint %r>" % self.name

    def __init__(self, title, category, description,
                 state, creator_first_name, creator_last_name, 
                 creator_telephone, creator_email, assigned_to, coordinate):
        """Constructor del modelo"""

        self.title = title
        self.category = category
        self.description = description
        self.state = state
        self.creator_first_name = creator_first_name
        self.creator_last_name = creator_last_name
        self.creator_telephone = creator_telephone
        self.creator_email = creator_email
        self.assigned_to = assigned_to
        self.coordinate = Coordinate(1, 2)


    @classmethod 
    def find_all_complaints(cls):
        """Devuelve todas las denuncias de la BD"""
        return Complaint.query.all()

    @classmethod
    def create_complaint(cls, title, category, description,
                 state, creator_first_name, creator_last_name, 
                 creator_telephone, creator_email, assigned_to, coordinate):
        """Crea una denuncia con los datos del formulario y la almacena en la BD"""

        new_complaint = Complaint(title, category, description,
                 state, creator_first_name, creator_last_name, 
                 creator_telephone, creator_email, assigned_to, coordinate)
        print("Insertando...............................", flush=True)
        db.session.add(new_complaint)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        "Retorna la denuncia correspondiente al id recibido por parámetro"

        return Complaint.query.get(id)
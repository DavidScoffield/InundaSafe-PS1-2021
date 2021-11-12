from sqlalchemy.sql.expression import join
from app.db import db
from app.helpers.config import actual_config
from sqlalchemy.orm import relationship
from app.models.coordinate import Coordinate
from app.models.category import Category
import datetime
from sqlalchemy import or_

from app.models.user import User

class Complaint(db.Model):
    """Modelo para las denuncias"""

    __tablename__ = "complaint"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    """category = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
    )"""
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship("Category")
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
        db.ForeignKey("users.id"),
        nullable=True,
    )
    coordinate = relationship("Coordinate", uselist=False)    #,cascade="all,delete", cascade="all,delete-orphan") ?. uselist=False es para one to one
    follow_ups = relationship("ComplaintFollowUp", cascade="all,delete-orphan")

    def __repr__(self):
        return "<Complaint %r>" % self.title

    def __init__(self, title, category, description,
                 creator_first_name, creator_last_name,
                 creator_telephone, creator_email, assigned_to, coordinate, state = "Sin Confirmar"):
        """Constructor del modelo"""
        "assigned_to y category tienen el objeto entero, se asigna solo su id en la fk al inicializar la Category"
        "assigned_to puede ser Null si no se le asigno un usuario a la Denuncia; category es obligatoria"

        self.title = title
        self.category = category
        self.description = description
        self.state = state
        self.creator_first_name = creator_first_name
        self.creator_last_name = creator_last_name
        self.creator_telephone = creator_telephone
        self.creator_email = creator_email
        self.assigned_to = assigned_to.id if assigned_to != None else None
        self.coordinate = Coordinate(coordinate[0], coordinate[1])

    def get_attributes(self):
        "Retorna un diccionario con los atributos de la denuncia"
        "Elimino algunos atributos porque los cargo en el controller correctamente"

        attributes = vars(self)
        del attributes["_sa_instance_state"]
        del attributes["assigned_to"]
        del attributes["coordinate"]

        return attributes

    @classmethod
    def all_complaints_paginated(cls, page_number: int = 1):
        ac = actual_config()
        elements_quantity = ac.elements_quantity
        
        return Complaint.query.paginate(
            max_per_page=elements_quantity,
            per_page=elements_quantity,
            page=page_number,
            error_out=True,
        )

    @classmethod
    def create_complaint(cls, **args):
        """Crea una denuncia con su coordenada con los datos del formulario y la almacena en la BD."""

        new_complaint = Complaint(**args)

        db.session.add(new_complaint)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        "Retorna la denuncia correspondiente al id recibido por parámetro"

        return Complaint.query.get(id)

    def find_my_assigned_user(self):
        """Devuelve el Objeto User (assigned_to) asociado a esta denuncia (self)"""
        
        return (User.query.get(self.assigned_to))
        
    def update_complaint(self, **args):
        """Actualizacion de la denuncia"""
        
        self.title = args["title"]
        self.category = args["category"]
        self.description = args["description"]
        self.state = args["state"]
        self.creator_first_name = args["creator_first_name"]
        self.creator_last_name = args["creator_last_name"]
        self.creator_telephone = args["creator_telephone"]
        self.creator_email = args["creator_email"]
        self.assigned_to = args["assigned_to"].id if args["assigned_to"] != None else None
        self.coordinate.latitude = args["coordinate"][0]
        self.coordinate.longitude = args["coordinate"][1]

        db.session.commit()

    
    def delete(self):
        "Borra una denuncia, junto con su Coordenada y sus Seguimientos"

        db.session.delete(self.coordinate)
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def delete_user_complaints(cls, user_id):
        """Elimina las denuncias activas que tengan a user_id como su usuario asignado"""

        user_complaints = Complaint.query.filter(Complaint.assigned_to == user_id).filter(
                or_(Complaint.state == "En Curso", Complaint.state == "Sin Confirmar")
            )

        for complaint in user_complaints:
            complaint.delete()

    @classmethod
    def search(
        cls,
        title: str = "",
        state: int = 1,      
    ):
        """
        Retorna una lista con todos las denuncias, teniendo en cuenta los filtros
        pasados por parametro, en caso que estos sean vacio retorna todas las denuncias.
        """

        ac = actual_config()
        order = ac.order_by
        return (
            Complaint.query
            .filter(Complaint.title.contains(title))
            .filter(Complaint.state.startswith(state))
            .order_by(eval(f"Complaint.title.{order}()"))
        )


    @classmethod
    def paginate(
        cls,
        complaints,
        page_number: int = 1,
    ):
        "Retorna la lista de denuncias pasadas por parametro paginados"
        ac = actual_config()
        elements_quantity = ac.elements_quantity
        return complaints.paginate(
            max_per_page=elements_quantity,
            per_page=elements_quantity,
            page=page_number,
            error_out=False,
        )
from app.db import db
from app.helpers.config import actual_config
from sqlalchemy.orm import relationship
from app.models.coordinate import Coordinate
from app.models.category import Category
import datetime

from app.models.user import User

class Complaint(db.Model):
    """Modelo para las denuncias"""

    __tablename__ = "complaint"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
    )
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
    follow_ups = relationship("ComplaintFollowUp")

    def __repr__(self):
        return "<Complaint %r>" % self.title

    def __init__(self, title, category, description,
                 state, creator_first_name, creator_last_name,
                 creator_telephone, creator_email, assigned_to, coordinate):
        """Constructor del modelo"""
        "assigned_to y category tienen el objeto entero, se asigna solo su id en la fk al inicializar la Category"
        "assigned_to puede ser Null si no se le asigno un usuario a la Denuncia; category es obligatoria"

        self.title = title
        self.category = category.id
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
        #del attributes["_sa_instance_state"]
        del attributes["assigned_to"]
        del attributes["category"]
        del attributes["coordinate"]

        return attributes

    @classmethod
    def find_all_complaints_and_their_categories(cls):
        """Devuelve todas las denuncias de la BD JOIN las Categorias de esas denuncias"""
        """Resulta en un conjunto de tuplas, donde [0] es la Complaint y [1] es la Category"""
        return db.session.query(Complaint, Category).join(Category, Complaint.category == Category.id).all()
        
        #Esto era para hacer join Complaint-User para devolver tambien al usuario asignado a esta denuncia.
        #return db.session.query(Complaint, User).join(User, Complaint.assigned_to == User.id).all()
        #devuelve Tuplas, [0] complaint y [1] el usuario asignado

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

    def find_my_category_and_assigned_user(self):
        """Devuelve los Objetos Category y User (assigned_to) asociados a esta denuncia (self)"""
        res = []
        res.append(Category.query.get(self.category))
        res.append(User.query.get(self.assigned_to))
        return res

    def update_complaint(self, **args):
        """Actualizacion de la denuncia"""
        
        self.title = args["title"]
        self.category = args["category"].id
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
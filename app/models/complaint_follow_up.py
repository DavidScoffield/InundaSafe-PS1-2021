from app.db import db
import datetime
from app.helpers.config import actual_config

class ComplaintFollowUp(db.Model):
    """Modelo para los seguimientos de las denuncias"""

    __tablename__ = "complaint_follow_up"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
    )
    complaint_id = db.Column(
        db.Integer, 
        db.ForeignKey("complaint.id"))
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return "<ComplaintFollowUp %r>" % self.description

    def __init__(self, author_id, description, complaint_id):
        """Constructor del modelo"""

        self.author_id = author_id
        self.description = description
        self.complaint_id = complaint_id
    

    @classmethod
    def create_follow_up(cls, description, author_id, complaint_id):
        """Crea un seguimiento con los datos del formulario y la almacena en la BD."""

        new_follow_up = ComplaintFollowUp(author_id, description, complaint_id)

        db.session.add(new_follow_up)
        db.session.commit()
    
    @classmethod
    def find_by_id(cls, id):
        "Retorna el seguimiento correspondiente al id recibido por parámetro"

        return ComplaintFollowUp.query.get(id)

    def update_follow_up(self, description):
        """Actualizacion del seguimiento"""

        self.description = description
        db.session.commit()
    
    def delete(self):
        "Borra un seguimiento"

        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def paginate(cls, id_complaint, page_number: int = 1):

        follow_ups = ComplaintFollowUp.query.filter(ComplaintFollowUp.complaint_id == id_complaint)
        "Retorna la lista de seguimientos pasados por parametro paginados"
        ac = actual_config()
        elements_quantity = ac.elements_quantity
        return follow_ups.paginate( 
            max_per_page=elements_quantity,
            per_page=elements_quantity,
            page=page_number,
            error_out=False
        )
        
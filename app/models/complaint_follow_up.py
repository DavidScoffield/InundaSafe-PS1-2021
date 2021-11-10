from app.db import db
import datetime

class ComplaintFollowUp(db.Model):
    """Modelo para los seguimientos de las denuncias"""

    __tablename__ = "complaint_follow_up"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"), #, ondelete="CASCADE" ?
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
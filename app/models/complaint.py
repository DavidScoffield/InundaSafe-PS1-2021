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
    coordinate = relationship("Coordinate", uselist=False)    #,cascade="all,delete", cascade="all,delete-orphan") ?. uselist=False es para one to one
    follow_ups = relationship("ComplaintFollowUp")

    def __repr__(self):
        return "<Complaint %r>" % self.name

    def __init__(self, title, category, description,
                 state, creator_first_name, creator_last_name, 
                 creator_telephone, creator_email, coordinate):
        """Constructor del modelo"""

        self.title = title
        self.category = category
        self.description = description
        self.state = state
        self.creator_first_name = creator_first_name
        self.creator_last_name = creator_last_name
        self.creator_telephone = creator_telephone
        self.creator_email = creator_email
        self.coordinate = Coordinate(coordinate[0], coordinate[1])


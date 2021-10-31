from app.db import db
from app.helpers.config import actual_config
from sqlalchemy.orm import relationship
from app.models.coordinate import Coordinate


class EvacuationRoute(db.Model):
    """Modelo para el manejo de la tabla EvacuationRoute de la base de datos"""

    __tablename__ = "evacuation_route"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(500))
    state = db.Column(db.String(100))
    coordinates = relationship("Coordinate")

    def __repr__(self):
        return "<EvacuationRoute %r>" % self.name

    def __init__(self, name, description, coordinates, state):
        """Constructor del modelo"""

        self.name = name
        self.description = description
        self.coordinates = [Coordinate(coordinate[0], coordinate[1]) for coordinate in coordinates]
        self.state = state

    @classmethod
    def new(cls, **args):
        "Recibe los parámetros para crear el recorrido de evacuación y lo guarda en la base de datos"
        
        evacuation_route = EvacuationRoute(**args)
        db.session.add(evacuation_route)
        db.session.commit()

    @classmethod
    def exists_name(cls, name):
        "Verifica si existe un recorrido de evacuación con el nombre recibido por parámetro"
        
        return (
            EvacuationRoute.query.filter(
                EvacuationRoute.name.ilike(name)
            ).first()
            is not None
        )
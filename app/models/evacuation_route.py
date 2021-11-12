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


    @classmethod
    def search(
        cls,
        page_number: int = 1,
        name: str = "",
        state: str = "",
    ):
        """
        Retorna una lista con todos los recorridos de evacuación, teniendo en cuenta los filtros pasados
        por parametro, en caso que estos sean vacíos retorna todos los recorridos de evacuación.
        Retorna el resultado paginado.
        """

        ac = actual_config()
        order = ac.order_by

        ordered_evacuation_routes = (
            EvacuationRoute.query.filter(
                EvacuationRoute.name.contains(name)
            )
            .filter(EvacuationRoute.state.startswith(state))
            .order_by(eval(f"EvacuationRoute.name.{order}()"))
        )

        paginated_evacuation_routes = EvacuationRoute.paginate(
            ordered_evacuation_routes, page_number
        )

        return paginated_evacuation_routes


    @classmethod
    def paginate(
        cls,
        evacuation_routes,
        page_number: int = 1,
    ):
        "Retorna la lista de recorridos de evacuación pasados por parametro paginados"

        ac = actual_config()
        elements_quantity = ac.elements_quantity
        
        paginated_evacuation_routes = evacuation_routes.paginate(
            max_per_page=elements_quantity,
            per_page=elements_quantity,
            page=page_number,
            error_out=False,
        )

        return paginated_evacuation_routes


    @classmethod
    def find_by_id(cls, id):
        "Retorna el recorrido de evacuación correspondiente al id recibido por parámetro"

        return EvacuationRoute.query.get(id)

    def delete_coordinates(self):
        "Borra las coordenadas del recorrido de evacuación"

        for coordinate in self.coordinates:
            db.session.delete(coordinate)
        db.session.commit()

    def delete(self):
        "Borra un recorrido de evacuación y sus coordenadas asociadas"
        
        self.delete_coordinates()
        db.session.delete(self)
        db.session.commit()


    def get_attributes(self, keep_instance_state = True):
        "Retorna un diccionario con los atributos del recorrido de evacuación"

        attributes = vars(self)
        attributes["coordinates"] = self.coordinates
        
        if not keep_instance_state:
            del attributes["_sa_instance_state"]

        return attributes


    def update(self, **args):
        "Actualiza los datos del recorrido de evacuación con los recibidos por parámetro"

        for attribute, value in args.items():
            if attribute == "coordinates":
                self.delete_coordinates()
                self.coordinates = [Coordinate(coordinate[0], coordinate[1]) for coordinate in value]
            else:
                setattr(self, attribute, value)

        db.session.commit()
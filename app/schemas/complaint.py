from marshmallow import Schema, fields, validate, validates_schema, post_load, post_dump
from marshmallow.exceptions import MarshmallowError
from app.helpers.validate_coordinates import validate_coordinates
from app.models.category import Category
from app.models.complaint import Complaint
import json

class ComplaintSchema(Schema):
    """
    Definición de los atributos y validadores del schema de complaints
    """

    title = fields.Str(data_key="titulo",
                       required = True,
                       validate=validate.Regexp("^[a-zA-Z ]+$"))

    category = fields.Raw(data_key="categoria_id",
                          required = True)

    description = fields.Str(data_key="descripcion",
                             required = True,
                             validate=validate.Regexp("^[a-zA-Z0-9 ]+$"))
    
    state = fields.Str(data_key="estado")

    coordinate = fields.Str(data_key="coordenadas", required = True)

    creator_first_name = fields.Str(data_key="nombre_denunciante",
                                    required = True,
                                    validate=validate.Regexp("^[a-zA-Z ]+$"))

    creator_last_name = fields.Str(data_key="apellido_denunciante",
                                   required = True,
                                   validate=validate.Regexp("^[a-zA-Z ]+$"))

    creator_telephone = fields.Str(data_key="telcel_denunciante", 
                                   required = True,
                                   validate=validate.Regexp("^[\d]+$"))

    creator_email = fields.Email(data_key="email_denunciante",
                                 required = True)

    def __init__(self, post_schema = False, **args):
        self.post_schema = post_schema
        super().__init__()


    @validates_schema
    def validate_coordinate(self, data, **kwargs):
        "Verifica que la coordenada ingresada sea válida"

        try:
            coordinate = data["coordinate"]
            coordinate = coordinate.replace(" ", "")
            coordinate = coordinate.split(",")
            if not validate_coordinates(coordinate):
                raise MarshmallowError
            
            data["coordinate"] = coordinate
        except:
            raise MarshmallowError
        
    @validates_schema
    def validate_category(self, data, **kwargs):
        "Verifica que la categoría ingresada exista"
        
        category = data["category"]
        if not isinstance(category, int):
            raise MarshmallowError

        category = Category.find_by_id(category)
        if not category:
            raise MarshmallowError

        data["category"] = category

    @post_load
    def create_complaint_object(self, data, **kwargs):
        "Crea la denuncia a partir de los datos del schema"

        return Complaint.create_complaint(**data)

    @post_dump
    def format_dump(self, data, **kwargs):
        "Formatea el dump del schema"

        if self.post_schema:
            data["categoria_id"] = data["categoria_id"].id
            del data["coordenadas"]
            del data["estado"]
        else:
            data["categoria"] = data["categoria_id"].name
            data["coordenadas"] = json.loads(data["coordenadas"])
            del data["categoria_id"]

        return data

complaint_post_schema = ComplaintSchema(post_schema = True, many=False)

complaint_get_schema = ComplaintSchema(many=False)

class PaginatedComplaintSchema(Schema):
    total = fields.Int()
    page = fields.Int(data_key="pagina")
    pages = fields.Int(data_key="paginas")
    per_page = fields.Int(data_key="por_pagina")
    items = fields.Nested(complaint_get_schema, many=True)

paginated_complaints_schema = PaginatedComplaintSchema()
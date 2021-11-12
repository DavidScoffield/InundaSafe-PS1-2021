from marshmallow import Schema, fields, validate, validates_schema, post_dump
from marshmallow.exceptions import MarshmallowError
from app.helpers.validate_coordinates import validate_coordinates
from app.models.category import Category
import json

class ComplaintSchema(Schema):

    """
    Definición de los atributos y validadores del schema de complaints
    """

    title = fields.Str(data_key="titulo",
                       required = True,
                       validate=validate.Regexp("^[a-zA-Z ]+$"))

    category = fields.Int(data_key="categoria_id",
                          required = True)

    description = fields.Str(data_key="descripcion",
                             required = True,
                             validate=validate.Regexp("^[a-zA-Z ]+$"))

    coordinate = fields.Str(data_key="coordenadas",
                            required = True)

    creator_first_name = fields.Str(data_key="apellido_denunciante",
                                    required = True,
                                    validate=validate.Regexp("^[a-zA-Z ]+$"))

    creator_last_name = fields.Str(data_key="nombre_denunciante",
                                   required = True,
                                   validate=validate.Regexp("^[a-zA-Z ]+$"))

    creator_telephone = fields.Str(data_key="telcel_denunciante", 
                                   required = True,
                                   validate=validate.Regexp("^[\d]+$"))

    creator_email = fields.Email(data_key="email_denunciante",
                                 required = True)

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

        category = Category.find_by_id(data["category"])
        if not category:
            raise MarshmallowError

        data["category"] = category

    @post_dump
    def format_dump(self, data, **kwargs):
        "Formatea el dump del schema"

        data["coordenadas"] = data["coordenadas"].replace("[", "").replace("]", "")
        
        return { "atributos" : data } 

complaint_schema = ComplaintSchema(many=False)
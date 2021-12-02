from flask import jsonify, Blueprint
from app.models.configuration import Configuration
import json

from app.schemas.color import ColorSchema

color_api = Blueprint("colors", __name__, url_prefix="/colors")

@color_api.get("/")
def get():
    colors = Configuration.actual()

    color_schema = ColorSchema()
    json_string = color_schema.dumps(colors.colors_public)

    return (json_string)
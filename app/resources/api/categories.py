from flask import jsonify, Blueprint
from app.models.category import Category
import json

from app.schemas.category import categories_schema

categories_api = Blueprint("categories", __name__, url_prefix="/categories")

@categories_api.get("/")
def get():
    categories = Category.find_all_categories()

    json_string = categories_schema.dumps(categories)

    return json_string
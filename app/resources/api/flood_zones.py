from flask import jsonify, Blueprint

flood_zones_api = Blueprint(
    "flood_zones", __name__, url_prefix="/zonas-inundables"
)


@flood_zones_api.get("/")
def index():

    return jsonify([])

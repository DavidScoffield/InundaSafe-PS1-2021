from flask import Blueprint
from flask.templating import render_template

config_routes = Blueprint("config_routes", __name__, url_prefix="/")


@config_routes.get("/")
def index():
    return render_template("config/index.html")

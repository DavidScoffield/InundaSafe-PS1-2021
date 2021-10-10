from flask import Blueprint
from flask.templating import render_template

from app.models.colors import Color
from app.models.configuration import Configuration

config_routes = Blueprint("config_routes", __name__, url_prefix="/config")


@config_routes.get("/")
def index():
    colors = Color.all()
    config_actual = Configuration.actual()

    return render_template("config/index.html", colors=colors, config=config_actual)

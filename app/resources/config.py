from flask import Blueprint, redirect, request, url_for, render_template
from app.models.colors import Color
from app.models.configuration import Configuration

config_routes = Blueprint("config_routes", __name__, url_prefix="/config")


@config_routes.get("/")
def index():
    colors = Color.all()
    config_actual = Configuration.actual()

    return render_template("config/index.html", colors=colors, config=config_actual)


@config_routes.post("/", endpoint="update")
def update():
    data = request.form

    Configuration.update(
        order_by=data["order_by"],
        elements_quantity=data["elements_quantity"],
        colors_id_public=data["color_public"],
        colors_id_private=data["color_private"],
    )

    return redirect(url_for("config_routes.index"))

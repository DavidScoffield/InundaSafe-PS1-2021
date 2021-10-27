from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
    render_template,
    abort,
    session,
    flash
)
from app.models.colors import Color
from app.models.configuration import Configuration
from app.helpers.auth import authenticated
from app.helpers.validators import is_empty
from app.helpers.check_permission import check_permission

config_routes = Blueprint(
    "config_routes", __name__, url_prefix="/config"
)


@config_routes.get("/")
def index():
    "Controller para mostrar el formulario para modificar los datos de configuracion de la aplicacion"

    if not authenticated(session):
        abort(401)

    if not check_permission("config_show"):
        abort(401)

    colors = Color.all()
    config_actual = Configuration.actual()

    return render_template(
        "config/index.html",
        colors=colors,
        config=config_actual,
    )


@config_routes.post("/", endpoint="update")
def update():
    "Controller para actualizar la configuracion de la aplicacion en base a los datos del formulario"

    if not authenticated(session):
        abort(401)

    if not check_permission("config_update"):
        abort(401)

    data = request.form

    if list(filter(lambda parametro: is_empty(parametro), list(data.values()))):
        flash("Por favor, complete todos los campos", category="config")
        return redirect(url_for("config_routes.index"))
    
    if not data["elements_quantity"].isnumeric():
        flash("Por favor, ingrese una cantidad de elementos válida", category="config")
        return redirect(url_for("config_routes.index"))

    if not data["order_by"] in ("asc", "desc"):
        flash("Por favor, ingrese un criterio de ordenamiento válido", category="config")
        return redirect(url_for("config_routes.index"))

    Configuration.update(
        order_by=data["order_by"],
        elements_quantity=data["elements_quantity"],
        colors_id_public=data["color_public"],
        colors_id_private=data["color_private"],
    )

    return redirect(url_for("config_routes.index"))
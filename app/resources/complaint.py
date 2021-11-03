#from app.models.evacuation_route import EvacuationRoute
from app.helpers.forms.complaint_form import (
    ComplaintForm
)
from flask import (
    render_template,
    Blueprint,
    request,
    flash,
    redirect,
    url_for,
    session,
    abort,
)
from app.db import db
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission
from app.helpers.check_param_search import (
    check_param,
)
from app.helpers.validate_coordinates import validate_coordinates
import json

complaint_route = Blueprint(
    "complaint", __name__, url_prefix="/denuncias"
)


@complaint_route.get("/new")
def new():
    "Controller para mostrar el formulario para el alta de una denuncia"

    if not authenticated(session) or not check_permission(
        "complaint_new"
    ):
        abort(401)

    form = ComplaintForm()

    return render_template("complaint/new.html", form=form)

"""
@complaint_route.post("/new")
def create():
    "Controller para crear el recorrido de evacuación a partir de los datos del formulario"
    
    if not authenticated(session) or not check_permission(
        "evacuation_route_create"
    ):
        abort(401)

    form = EvacuationRouteForm(request.form)
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores",
              category="evacuation_route_new")
    else:
        args = form.data
        del args["submit"]
        del args["csrf_token"]
        del args["id"]
        if EvacuationRoute.exists_name(args["name"]):
            flash("Ya existe un recorrido de evacuación con ese nombre",
                   category="evacuation_route_new")
        else:
            args["coordinates"] = json.loads(args["coordinates"])
            for coordinate in args["coordinates"]:
                if not validate_coordinates(coordinate):
                    flash("Se ingresó una coordenada inválida", category="evacuation_route_new")
                    return render_template("evacuation_route/new.html", form=form)

            EvacuationRoute.new(**args)
            flash("Recorrido de evacuación agregado exitosamente",
                   category="evacuation_route_new")

    return render_template("evacuation_route/new.html", form=form)
    """
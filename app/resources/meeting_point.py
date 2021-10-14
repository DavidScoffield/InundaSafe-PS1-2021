from app.models.meeting_point import MeetingPoint
from app.helpers.forms.meeting_point_form import MeetingPointForm
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

meeting_point = Blueprint("meeting_point", __name__, url_prefix="/meeting-point")

@meeting_point.get("/new")
def new():
    "Controller para mostrar el formulario para el alta de un punto de encuentro"

    if not authenticated(session) or not check_permission("punto_encuentro_new"):
        abort(401)

    form = MeetingPointForm()

    return render_template("meeting_point/new.html", form=form)


@meeting_point.post("/new")
def create():
    "Controller para crear el punto de encuentro a partir de los datos del formulario"
    
    if not authenticated(session) or not check_permission("punto_encuentro_create"):
        abort(401)

    form = MeetingPointForm(request.form)
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores")
    else:
        args = form.data
        del args["submit"]
        del args["csrf_token"]
        if MeetingPoint.exists_address(args["address"]):
            flash("Ya existe un punto de encuentro con esa dirección")
        else:
            MeetingPoint.new(**args)
            flash("Punto de encuentro agregado exitosamente")

    return redirect(url_for("meeting_point.new"))


@meeting_point.route("/<int:page_number>")
def index(page_number):
    "Controller para mostrar el listado de puntos de encuentro"

    if not authenticated(session) or not check_permission("punto_encuentro_index"):
        abort(401)

    meeting_points = MeetingPoint.paginate(page_number)

    return render_template("meeting_point/index.html", meeting_points = meeting_points)

@meeting_point.post("/delete")
def destroy():

    if not authenticated(session) or not check_permission("punto_encuentro_destroy"):
        abort(401)

    MeetingPoint.delete(request.form["id_meeting_point"])

    flash("Punto de encuentro borrado exitosamente")

    return redirect(url_for("meeting_point.index", page_number=1))
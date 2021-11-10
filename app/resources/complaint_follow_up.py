from app.models.complaint import Complaint
from app.models.complaint_follow_up import ComplaintFollowUp
from app.models.user import User
from app.helpers.forms.follow_up_form import (
    FollowUpForm
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
import json
from app.helpers.validate_coordinates import validate_coordinates

follow_up_route = Blueprint(
    "follow_up", __name__, url_prefix="/seguimientos"
)

@follow_up_route.get("/")
def index():
    "Listado de los seguimientos"

    if not authenticated(session) or not check_permission(
        "follow_up_index"
    ):
        abort(401)
    

@follow_up_route.post("/new")
def new():
    "Controller para mostrar el formulario para el alta de un seguimiento"

    if not authenticated(session) or not check_permission(
        "follow_up_new"
    ):
        abort(401)

    id_complaint = request.form["id_complaint"]
    form = FollowUpForm(request.form)
    user = User.find_user_by_id(session["user"])

    return render_template("follow_up/new.html", form=form, user=user, id_complaint=id_complaint)


@follow_up_route.post("/create")
def create():
    "Controller para crear un seguimiento a partir de los datos del formulario"
    
    if not authenticated(session) or not check_permission(
        "follow_up_create"
    ):
        abort(401)

    form = FollowUpForm(request.form)
    args = form.data
    complaint_id = args["id_complaint"]

    user = User.find_user_by_id(session["user"])
    
    # Validacion de los campos
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores", category="follow_up_new")
        return render_template("follow_up/new.html", form=form, user=user, complaint_id=complaint_id)
    
    del args["submit"]
    del args["csrf_token"]
    description = args["description"]
    
    ComplaintFollowUp.create_follow_up(description, session["user"], complaint_id)

    flash("Seguimiento creado correctamente", category="follow_up_new")
    return render_template("follow_up/new.html", form=form, user=user, id_complaint=complaint_id)

    
    
    
  
@follow_up_route.post("/edit")
def edit():
    "Controller para editar seguimiento"

    if not authenticated(session) or not check_permission(
        "follow_up_edit"
    ):
        abort(401)
    

@follow_up_route.post("/destroy")
def destroy():
    "Controller para eliminar seguimiento"

    if not authenticated(session) or not check_permission(
        "follow_up_destroy"
    ):
        abort(401)
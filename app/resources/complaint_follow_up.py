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
    

@follow_up_route.get("/new")
def new():
    "Controller para mostrar el formulario para el alta de un seguimiento"

    if not authenticated(session) or not check_permission(
        "follow_up_new"
    ):
        abort(401)

    form = FollowUpForm()
    user = User.find_user_by_id(session["user"])

    return render_template("follow_up/new.html", form=form, user=user)


@follow_up_route.post("/new")
def create():
    "Controller para crear un seguimiento a partir de los datos del formulario"
    
    if not authenticated(session) or not check_permission(
        "follow_up_create"
    ):
        abort(401)
    


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

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
    return redirect(url_for("complaint.show", comp_id=complaint_id)) #En complaint.show entra como un GET.

  
@follow_up_route.post("/edit")
def edit():
    "Controller para mostrar el form para editar un seguimiento"

    if not authenticated(session) or not check_permission(
        "follow_up_edit"
    ):
        abort(401)
    
    id_follow_up = request.form["id_follow_up"]
    follow_up = ComplaintFollowUp.find_by_id(id_follow_up)
    author_follow_up = User.find_user_by_id(follow_up.author_id)
 
    #Le doy al form la descripción que está en la BD para el seguimiento específico
    form = FollowUpForm(description=follow_up.description, id=id_follow_up)

    return render_template(
        "follow_up/edit.html", follow_up=follow_up, form=form, author_follow_up=author_follow_up
    )


@follow_up_route.post("/update")
def update():
    """Controller para actualizar el seguimiento en la BD"""

    if not authenticated(session) or not check_permission(
        "follow_up_update"
    ):
        abort(401)
    
    form = FollowUpForm(request.form)
    args = form.data

    #seguimiento a actualizar
    follow_up = ComplaintFollowUp.find_by_id(args["id"])

    author_follow_up = User.find_user_by_id(follow_up.author_id)

    # Validacion de campos
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores", category="follow_up_update")
        return render_template("follow_up/edit.html", follow_up=follow_up, form=form, author_follow_up=author_follow_up)

    del args["submit"]
    del args["csrf_token"]

    #actualizo el seguimiento en la BD
    follow_up.update_follow_up(args["description"])

    flash("Seguimiento actualizado correctamente", category="follow_up_update")
    
    return redirect(url_for("complaint.show", comp_id=follow_up.complaint_id)) #En complaint.show entra como un GET.
    
    #return render_template(
    #    "follow_up/edit.html", follow_up=follow_up, form=form, author_follow_up=author_follow_up
    #)
    

@follow_up_route.post("/destroy")
def destroy():
    "Controller para eliminar seguimiento"

    if not authenticated(session) or not check_permission(
        "follow_up_destroy"
    ):
        abort(401)
    
    id_follow_up = request.form["id_follow_up"]
    follow_up = ComplaintFollowUp.find_by_id(id_follow_up)

    if not follow_up:
        flash("No se encontró el seguimiento",
               category="follow_up_delete")
    else:
        follow_up.delete()
        flash("Seguimiento borrado exitosamente",
               category="follow_up_delete")

    return redirect(url_for("complaint.index", page_number=1))
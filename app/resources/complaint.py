from app.models.complaint import Complaint
from app.models.complaint_follow_up import ComplaintFollowUp
from app.models.user import User
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
import json
from app.helpers.validate_coordinates import validate_coordinates

complaint_route = Blueprint(
    "complaint", __name__, url_prefix="/denuncias"
)

@complaint_route.get("/")
def index():
    "Listado de las denuncias"

    if not authenticated(session) or not check_permission(
        "complaint_index"
    ):
        abort(401)
    
    complaints = Complaint.find_all_complaints_and_their_categories()
    #complaints es un conjunto de tuplas con el siguiente formato: [Complaint, Category]

    return render_template(
        "complaint/index.html", complaints=complaints
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


@complaint_route.post("/new")
def create():
    "Controller para crear una denuncia a partir de los datos del formulario"
    
    if not authenticated(session) or not check_permission(
        "complaint_create"
    ):
        abort(401)
    
    form = ComplaintForm(request.form)
    args = form.data
    
    args["coordinate"] = json.loads(args["coordinate"])
    # Validacion de la coordenada
    if not validate_coordinates(args["coordinate"]):
        flash("Se ingresó una coordenada inválida", category="complaint_new")
        return render_template("complaint/new.html", form=form)

    # Validacion del resto de los campos
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores", category="complaint_new")
        return render_template("complaint/new.html", form=form)

    del args["submit"]
    del args["csrf_token"]
    Complaint.create_complaint(**args)

    flash("Denuncia creada correctamente", category="complaint_index")
    return redirect(url_for("complaint.index"))


@complaint_route.post("/show")
def show():
    "Controller para mostrar la información de una denuncia"

    if not authenticated(session) or not check_permission(
        "complaint_show"
    ):
        abort(401)
    
    id_complaint = request.form["id_complaint"]
    complaint = Complaint.find_by_id(id_complaint)
 
    if not complaint:
        flash("No se encontró la denuncia",
               category="complaint_show")
        return redirect(url_for("complaint.index"))
    
    lista = []
    for a in complaint.follow_ups:
        author = User.find_user_by_id(a.author_id)
        lista.append(author.username) 

    return render_template(
        "complaint/show.html",
        complaint=complaint, lista=lista
    )


@complaint_route.post("/edit")
def edit():
    "Controller para editar denuncia"

    if not authenticated(session) or not check_permission(
        "complaint_edit"
    ):
        abort(401)

    

@complaint_route.post("/destroy")
def destroy():
    "Controller para eliminar denuncia"

    if not authenticated(session) or not check_permission(
        "complaint_destroy"
    ):
        abort(401)
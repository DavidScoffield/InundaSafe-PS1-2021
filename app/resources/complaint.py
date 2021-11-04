from app.models.complaint import Complaint
from app.models.complaint_follow_up import ComplaintFollowUp
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

    #devuelve Tuplas, [0] complaint y [1] el usuario asignado
    #https://www.youtube.com/watch?v=_HIY1lZKEw0&ab_channel=PrettyPrinted
    complaints = Complaint.find_all_complaints()

    print("---------------------------------------------------", flush=True)
    for complaint in complaints:
        print(complaint, flush=True)
    print("---------------------------------------------------", flush=True)
    


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

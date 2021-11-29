from app.models.category import Category
from app.models.complaint import Complaint
from app.models.user import User
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
from app.helpers.check_param_search import (
    check_param,
)
from app.helpers.is_admin_or_is_my_complaint import is_admin_or_is_my_complaint
import datetime

complaint_route = Blueprint(
    "complaint", __name__, url_prefix="/denuncias"
)


@complaint_route.get("/<int:page_number>")
def index(page_number):
    "Listado de las denuncias"

    if not authenticated(session) or not check_permission(
        "complaint_index"
    ):
        abort(401)

    args = request.args
    title = args.get("title")
    state = args.get("state")

    """
       Busqueda por fechas:
       Recibe las fechas, las formatea para crear el objeto datetime
       Si no recibe la fecha minima la setea como la minima fecha representable (0001-01-01 00:00:00)
       Si no recibe la fecha maxima la setea como la maxima fecha representable (9999-12-31 23:59:59.999999)
       Si el usuario envia la fecha fin < fecha inicio, las invierte
    """
    init_date = args.get("init_date") #String: 2021-12-15. Si no cargan nada es un String vacio ''
    if(init_date):
        string_init_date = init_date.split('-') #List de Strings: ['2021', '12', '15']
        integer_map = map(int, string_init_date)
        int_init_date = list(integer_map) #List de Ints: [2021, 12, 15]
        init_date = datetime.datetime(int_init_date[0], int_init_date[1], int_init_date[2]) #Objeto datetime (time en 0)
    else:
        init_date = datetime.datetime.min

    end_date = args.get("end_date")
    if(end_date):
        string_end_date = end_date.split('-')
        integer_map = map(int, string_end_date)
        int_end_date = list(integer_map)
        end_date = datetime.datetime(int_end_date[0], int_end_date[1], int_end_date[2])
    else:
        end_date = datetime.datetime.max

    if(init_date > end_date):
        aux = init_date
        init_date = end_date
        end_date = aux

    title = check_param("@complaint/title", title)
    state = check_param("@complaint/state", state)

    complaints = Complaint.search(
        title=title,
        state=state,
        init_date=init_date,
        end_date=end_date,
    )

    if not complaints.first():
        flash("No se encontraron resultados", category="complaint_index_search")
        found_complaints = False
    else:
        found_complaints = True

    paginated_complaints = Complaint.paginate(
        page_number=page_number,
        complaints=complaints
    )

    # En caso que no encuentre ningun resultado se redirige a la pagina 1 con los argumentos de busqueda
    if (
        paginated_complaints.page != 1
        and paginated_complaints.page > paginated_complaints.pages
    ):
        # Si la cantidad de paginas es 0, se redirigira a la pagina 1
        if paginated_complaints.pages > 0:
            page = paginated_complaints.pages
        else:
            page = 1

        return redirect(
            url_for(
                "complaint.index",
                page_number=page,
                **request.args
            )
        )

    return render_template(
        "complaint/index.html", complaints=paginated_complaints, found_complaints=found_complaints
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
    del args["id"]

    Complaint.create_complaint(**args)

    flash("Denuncia creada correctamente", category="complaint_index")
    return redirect(url_for("complaint.index", page_number=1))

@complaint_route.route("/show", methods=('GET', 'POST'))
def show():
    "Controller para mostrar la información de una denuncia"

    if not authenticated(session) or not check_permission(
        "complaint_show"
    ):
        abort(401)

    if (request.method == 'POST'):
        id_complaint = request.form["id_complaint"]
        page_number = 1
    else:
        id_complaint = request.args.get('comp_id', type=int)
        page_number = request.args.get('page_number', type=int)

    complaint = Complaint.find_by_id(id_complaint)

    if not complaint:
        flash("No se encontró la denuncia",
               category="complaint_show")
        return redirect(url_for("complaint.index", page_number=1))

    complaint_assigned_user = complaint.find_my_assigned_user()

    paginated_follow_ups = ComplaintFollowUp.paginate(
        id_complaint=id_complaint,
        page_number=page_number,
    )

    lista = []
    for a in paginated_follow_ups.items:
        author = User.find_user_by_id(a.author_id)
        lista.append(author.username) 

    return render_template(
        "complaint/show.html",
        complaint=complaint, 
        paginated_follow_ups=paginated_follow_ups,
        lista=lista, 
        complaint_assigned_to=complaint_assigned_user
    )

@complaint_route.post("/edit")
def edit():
    "Controller para mostrar el form para editar denuncia"

    if not authenticated(session) or not check_permission(
        "complaint_edit"
    ):
        abort(401)

    id_complaint = request.form["id_complaint"]
    complaint = Complaint.find_by_id(id_complaint)
    
    #Estas lineas son para que por defecto muestre bien assigned_to y coordinate correctamente al renderizar el form
    #complaint tiene en assigned_to el id del User (o None), WTF necesita el Objeto completo, no solo su id.
    if(complaint.assigned_to == None):
        assigned_to = None
    else:
        assigned_to = User.find_user_by_id(complaint.assigned_to)

    #Lat y lng son strings, los hago float para que el mapa lo pinte bien
    coord = [float(complaint.coordinate.latitude), float(complaint.coordinate.longitude)]
 
    #Le doy al form los objetos en esos campos y la coordenada formateada a float
    form = ComplaintForm(**complaint.get_attributes(), assigned_to=assigned_to, coordinate=coord)

    return render_template(
        "complaint/edit.html", complaint=complaint, form=form
    )

@complaint_route.post("/update")
def update():
    """Controller para actualizar la denuncia en la BD"""

    if not authenticated(session) or not check_permission(
        "complaint_update"
    ):
        abort(401)

    form = ComplaintForm(request.form)
    args = form.data
    
    #complaint a actualizar
    complaint = Complaint.find_by_id(args["id"])

    #Si intento editar una Denuncia sin ser admin ni el asignado a esa Denuncia: abort
    if(not is_admin_or_is_my_complaint(complaint)):
        abort(401)

    args["coordinate"] = json.loads(args["coordinate"])
    # Validacion de la coordenada
    if not validate_coordinates(args["coordinate"]):
        flash("Se ingresó una coordenada inválida", category="complaint_update")
        return render_template("complaint/edit.html", complaint=complaint, form=form)

    # Validacion del resto de los campos
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores", category="complaint_update")
        return render_template("complaint/edit.html", complaint=complaint, form=form)

    del args["submit"]
    del args["csrf_token"]
    
    #actualizo la denuncia en la BD
    complaint.update_complaint(**args)

    flash("Denuncia actualizada correctamente", category="complaint_update")
    return render_template(
        "complaint/edit.html", complaint=complaint, form=form
    )

@complaint_route.post("/destroy")
def destroy():
    "Controller para eliminar denuncia"

    if not authenticated(session) or not check_permission(
        "complaint_destroy"
    ):
        abort(401)

    id_complaint = request.form["id_complaint"]
    complaint = Complaint.find_by_id(id_complaint)

    if not complaint:
        flash("No se encontró la denuncia",
               category="complaint_destroy")
    else:
        complaint.delete()
        flash("Denuncia borrada exitosamente",
               category="complaint_destroy")

    return redirect(url_for("complaint.index", page_number=1))
from app.models.evacuation_route import EvacuationRoute
from app.helpers.forms.evacuation_route_form import (
    EvacuationRouteForm
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

evacuation_route = Blueprint(
    "evacuation_route", __name__, url_prefix="/evacuation-route"
)


@evacuation_route.get("/new")
def new():
    "Controller para mostrar el formulario para el alta de un recorrido de evacuación"

    if not authenticated(session) or not check_permission(
        "evacuation_route_new"
    ):
        abort(401)

    form = EvacuationRouteForm()

    return render_template("evacuation_route/new.html", form=form)


@evacuation_route.post("/new")
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
        args = form.evacuation_route_data()
        EvacuationRoute.new(**args)
        flash("Recorrido de evacuación agregado exitosamente",
                category="evacuation_route_new")

    return render_template("evacuation_route/new.html", form=form)


@evacuation_route.get("/<int:page_number>")
def index(page_number):
    """
    Controller para mostrar el listado de recorridos de evacuación
    Recibe como parametro el numero de la pagina a mostrar
    Puede recibir como argumentos:
    - name : string -> campo de filtro para los nombres de recorridos de evacuación
    - state : string -> campo de filtro para los estados (publicado, despublicado) de recorridos de evacuación
    """

    if not authenticated(session) or not check_permission(
        "evacuation_route_index"
    ):
        abort(401)

    args = request.args
    name = args.get("name")
    state = args.get("state")

    name = check_param("@evacuation_route/name", name, "evacuation_route")
    state = check_param("@evacuation_route/state", state, "evacuation_route")

    evacuation_routes = EvacuationRoute.search(
        page_number=page_number,
        state=state,
        name=name,
    )

    if not evacuation_routes.pages:
        found_evacuation_routes = False
        flash("No se encontraron resultados", category="evacuation_route_index")
    else:
        found_evacuation_routes = True

    # En caso que no encuentre ningun resultado resultado se redirige a la pagina 1 con los argumentos de busqueda
    if (
        evacuation_routes.page != 1
        and evacuation_routes.page > evacuation_routes.pages
    ):
        # Si la cantidad de paginas es 0, se redirigira a la pagina 1
        if evacuation_routes.pages > 0:
            page = evacuation_routes.pages
        else:
            page = 1

        return redirect(
            url_for(
                "evacuation_route.index",
                page_number=page,
                **request.args
            )
        )

    return render_template(
        "evacuation_route/index.html",
        evacuation_routes=evacuation_routes,
        found_evacuation_routes=found_evacuation_routes
    )

@evacuation_route.post("/delete")
def destroy():
    "Controller para eliminar un recorrido de evacuación"

    if not authenticated(session) or not check_permission(
        "evacuation_route_destroy"
    ):
        abort(401)

    id_evacuation_route = request.form["id_evacuation_route"]
    evacuation_route = EvacuationRoute.find_by_id(id_evacuation_route)

    if not evacuation_route:
        flash("No se encontró el recorrido de evacuación",
               category="evacuation_route_delete")
    else:
        evacuation_route.delete()
        flash("Recorrido de evacuación borrado exitosamente",
               category="evacuation_route_delete")

    return redirect(url_for("evacuation_route.index", page_number=1))


@evacuation_route.post("/edit")
def edit():
    "Controller para mostrar el formulario para la modificación de un recorrido de evacuación"

    if not authenticated(session) or not check_permission(
        "evacuation_route_edit"
    ):
        abort(401)

    id_evacuation_route = request.form["id_evacuation_route"]

    evacuation_route = EvacuationRoute.find_by_id(id_evacuation_route) # ruta de evacuación que se quiere modificar

    if not evacuation_route:
        flash("No se encontró el recorrido de evacuación",
              category="evacuation_route_update")
        return redirect(url_for("evacuation_route.index", page_number=1))
    
    # se inicializa el formulario con los datos originales de la ruta de evacuación que se desea modificar
    form = EvacuationRouteForm(**evacuation_route.get_attributes())

    return render_template("evacuation_route/edit.html", form=form)


@evacuation_route.post("/update")
def update():
    "Controller para modificar el recorrido de evacuación a partir de los datos del formulario"

    if not authenticated(session) or not check_permission(
        "evacuation_route_update"
    ):
        abort(401)

    form = EvacuationRouteForm(request.form)

    if not form.validate_on_submit():
        flash("Por favor, corrija los errores",
              category="evacuation_route_update")
    else:
        args = form.evacuation_route_data()
        evacuation_route = EvacuationRoute.find_by_id(form.data["id"])
        evacuation_route.update(**args)
        flash("Recorrido de evacuación modificado exitosamente",
              category="evacuation_route_update")

    return render_template(
        "evacuation_route/edit.html",
        form=form,
        id_evacuation_route=form.data["id"]
    )


@evacuation_route.post("/show")
def show():
    "Controller para mostrar la información de un recorrido de evacuación"

    if not authenticated(session) or not check_permission(
        "evacuation_route_show"
    ):
        abort(401)

    id_evacuation_route = request.form["id_evacuation_route"]
    evacuation_route = EvacuationRoute.find_by_id(id_evacuation_route)

    if not evacuation_route:
        flash("No se encontró el recorrido de evacuación",
               category="evacuation_route_show")

        return redirect(url_for("evacuation_route.index", page_number=1))

    return render_template(
        "evacuation_route/show.html",
        evacuation_route=evacuation_route,
    )
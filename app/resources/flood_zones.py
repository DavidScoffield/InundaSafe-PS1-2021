from app.models.flood_zones import FloodZones
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
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission

flood_zones = Blueprint(
    "flood_zones", __name__, url_prefix="/flood-zones"
)


@flood_zones.get("/<int:page_number>")
def index(page_number):
    """
    Controller para mostrar el listado de zonas inundables
    Recibe como parametro el numero de la pagina a mostrar
    Puede recibir como argumentos:
    - name : string -> campo de filtro para los nombres de las zonas inundables
    - state : string -> campo de filtro para los estados(publicado, despublicado) de las zonas inundables
    """

    if not authenticated(session) or not check_permission(
        "punto_encuentro_index"
    ):
        abort(401)

    # args = request.args
    # name = args.get("name")
    # state = args.get("state")

    # name = check_param("@meeting_point/name", name)
    # state = check_param("@meeting_point/state", state)

    # meeting_points = MeetingPoint.search(
    #     page_number=page_number,
    #     state=state,
    #     name=name,
    # )

    # # En caso que no encuentre ningun resultado resultado se redirige a la pagina 1 con los argumentos de busqueda
    # if (
    #     meeting_points.page != 1
    #     and meeting_points.page > meeting_points.pages
    # ):
    #     # Si la cantidad de paginas es 0, se redirigira a la pagina 1
    #     if meeting_points.pages > 0:
    #         page = meeting_points.pages
    #     else:
    #         page = 1

    #     return redirect(
    #         url_for(
    #             "meeting_point.index",
    #             page_number=page,
    #             **request.args
    #         )
    #     )

    return render_template(
        "flood_zones/index.html",
        flood_zones=flood_zones,
    )

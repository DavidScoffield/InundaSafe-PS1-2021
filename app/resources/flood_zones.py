import os
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
    current_app,
)
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission
from app.helpers.upload_flood_zones import (
    allowed_file,
    read_file,
    remove_file_filesystem,
    save_data,
    save_file_filesystem,
    validate_coor_quantity,
)

from app.helpers.logger import looger_error


flood_zones = Blueprint(
    "flood_zones", __name__, url_prefix="/flood-zones"
)


@flood_zones.get("/<int:page_number>")
def index(page_number: int = 1):
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


# @flood_zones.get("/upload", endpoint="show_upload")
# def show_load_flood_zones():

#     "Controller para crear el punto de encuentro a partir de los datos del formulario"

#     if not authenticated(session) or not check_permission(
#         "zonas_inundables_import"
#     ):
#         abort(401)

#     return render_template("flood_zones/load.html")


@flood_zones.post("/upload", endpoint="upload")
def upload_flood_zones():

    if not authenticated(session) or not check_permission(
        "zonas_inundables_import"
    ):
        abort(401)

    # check if the post request has the file part
    if "csv_file" not in request.files:
        flash(
            "Falla en carga de archivo",
            category="flood_zones_import",
        )
        return redirect(
            url_for("flood_zones.index", page_number=1)
        )
    file = request.files["csv_file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("Por favor seleccione un archivo .csv")
        return redirect(
            url_for("flood_zones.index", page_number=1)
        )
    if file and allowed_file(file.filename):
        try:
            # Save
            file_path = save_file_filesystem(
                file, current_app
            )

            # Read file
            (data, error) = read_file(file_path)

            # TODO: Chequear que se ingrasan la cantidad de paraemtros requeridos -- es necesario?

            # Validate quantity of coordinate in witch of one zone
            (data, error) = validate_coor_quantity(
                data=data, error=error
            )

            # TODO: Guardar o actualizar los datos validos en la BD
            save_data(data)

            #! TODO: cuando ocurre un problema el remove nunda se ejecuta, solucionar. Quizas pasarlo a un `finally` o algo asi
            # Remove file
            remove_file_filesystem(file_path)
        except Exception as err:
            looger_error(f" - ERROR: {err}")
            flash(
                "Ocurrio un error al cargar el archivo, compruebe que el formato del archivo sea valido",
                category="flood_zones_import",
            )
            return redirect(
                url_for("flood_zones.index", page_number=1)
            )

        flash(
            f"{len(data)} datos guardados en el sistema. {len(error)} datos descartados por errores.",
            category="flood_zones_import",
        )

    return redirect(
        url_for("flood_zones.index", page_number=1)
    )

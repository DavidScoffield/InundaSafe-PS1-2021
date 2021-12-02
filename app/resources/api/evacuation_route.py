from flask import jsonify, Blueprint, abort, request
from werkzeug.exceptions import NotFound
from app.models.evacuation_route import EvacuationRoute
from app.schemas.evacuation_route import (
    evacuation_routes_paginated_schema,
)
from app.helpers.validators import (
    validate_params_pagination,
    validate_received_params,
)

from app.helpers.logger import (
    logger_error,
    logger_exception,
)

evacuation_route_api = Blueprint(
    "evacuation_route",
    __name__,
    url_prefix="/recorridos-evacuacion",
)


@evacuation_route_api.get("/")
def getAll():
    """
    Controller de la api para recuperar la informacion de recorridos de evacuacion.
    Se pagina en base a la configuracion del sistema
    @params:
        - pagina: int
    """
    try:
        try:
            if not validate_received_params(
                request.args
            ):
                abort(404)

            page = request.args.get("pagina", None)

            (page, per_page) = validate_params_pagination(
                page
            )
        except:
            abort(
                404,
                {
                    "custom_description": "Los argumentos enviados son invalidos, asegurese de enviarlos correctamente."
                },
            )

        try:
            evacuation_routes = EvacuationRoute.all(
                page=page, per_page=per_page
            )
        except NotFound:
            abort(
                404,
                {
                    "custom_description": "No hay recorridos de evacuacion en base a los parametros ingresados."
                },
            )

        if not evacuation_routes or not evacuation_routes.total:
            abort(
                404,
                {
                    "custom_description": "No hay recorridos de evacuacion disponibles."
                },
            )

        evacuation_route_dumped = (
            evacuation_routes_paginated_schema.dump(
                evacuation_routes
            )
        )

        return jsonify(recorridos=evacuation_route_dumped)

    except NotFound as err:
        raise
    except Exception as err:
        logger_error(err)
        logger_exception(err.__doc__)
        abort(500)

from flask import jsonify, Blueprint, abort, request
from werkzeug.exceptions import NotFound
from app.models.meeting_point import MeetingPoint
from app.schemas.meeting_point import (
    meeting_points_paginated_schema,
)
from app.helpers.validators import (
    validate_params_pagination,
    validate_received_params,
)

from app.helpers.logger import (
    logger_error,
    logger_exception,
)

meeting_point_api = Blueprint(
    "meeting_point",
    __name__,
    url_prefix="/puntos-encuentro",
)


@meeting_point_api.get("/")
def getAll():
    """
    Controller de la api para recuperar la informacion de puntos de encuentro.
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
            meeting_points = MeetingPoint.all(
                page=page, per_page=per_page
            )
        except NotFound:
            abort(
                404,
                {
                    "custom_description": "No hay puntos de encuentro en base a los parametros ingresados."
                },
            )

        if meeting_points.total == 0:
            abort(
                404,
                {
                    "custom_description": "No hay puntos de encuentro disponibles."
                },
            )

        evacuation_route_dumped = (
            meeting_points_paginated_schema.dump(
                meeting_points
            )
        )

        return jsonify(
            puntos_encuentro=evacuation_route_dumped
        )

    except NotFound as err:
        raise
    except Exception as err:
        logger_error(err)
        logger_exception(err.__doc__)
        abort(500)

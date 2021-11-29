from flask import jsonify, Blueprint, abort, request
from werkzeug.exceptions import NotFound
from app.models.flood_zones import FloodZones
from app.schemas.flood_zones import (
    flood_zone_schema,
    flood_zones_paginate_schema,
)
from app.helpers.validators import (
    validate_params_pagination,
    validate_received_params,
)

from app.helpers.logger import (
    logger_error,
    logger_exception,
    logger_info,
)

flood_zones_api = Blueprint(
    "flood_zones", __name__, url_prefix="/zonas-inundables"
)


@flood_zones_api.get("/")
def getAll():
    """
    Controller de la api para recuperar la informacion de zonas inundables.
    Se pagina en base a la configuracion del sistema
    @params:
        - pagina: int
    """
    try:
        try:
            if not validate_received_params(
                request.args.keys()
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
            flood_zones = FloodZones.all(
                page=page, per_page=per_page
            )
        except NotFound:
            abort(
                404,
                {
                    "custom_description": "No hay zonas inundables en base a los parametros ingresados."
                },
            )

        if flood_zones.total == 0:
            abort(
                404,
                {
                    "custom_description": "No hay zonas inundables disponibles."
                },
            )

        flood_zone_dumped = (
            flood_zones_paginate_schema.dump(flood_zones)
        )

        return jsonify(zonas=flood_zone_dumped)

    except NotFound as err:
        raise
    except Exception as err:
        logger_error(err)
        logger_exception(err.__doc__)
        abort(500)


@flood_zones_api.get("/<int:id>")
def getById(id: int = None):
    """
    Controller de la api para recuperar la informacion de una zona inundable
    por id (pasado por url)
    """
    try:
        flood_zone = FloodZones.find_by_id(
            id, mustBeActive=True
        )
        if not flood_zone:
            abort(404)

        flood_zone_dumped = flood_zone_schema.dump(
            flood_zone
        )

        return jsonify(atributos=flood_zone_dumped)

    except NotFound:
        raise
    except Exception as err:
        logger_error(err)
        abort(500)

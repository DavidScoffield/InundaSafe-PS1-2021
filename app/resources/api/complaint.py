from flask import jsonify, Blueprint, request, abort
from app.models.complaint import Complaint
from app.schemas.complaint import (complaint_post_schema as complaint_schema, 
                                   paginated_complaints_schema)
from marshmallow.exceptions import MarshmallowError
from werkzeug.exceptions import BadRequest, NotFound
from app.helpers.validators import (
    validate_params_pagination,
    validate_received_params,
)
import json

complaint_api = Blueprint("complaint", __name__, url_prefix="/denuncias")


@complaint_api.post("/")
def create():
    """
    Controller de la api para crear una denuncia a partir de los datos recibidos por post
    
      - Si algún campo posee errores se informará con un mensaje y se retornará un código 400

      - Si ocurre algún error inesperado se informará con un mensaje y se retornará un código 500

      - Si no hay errores se crea la denuncia y como respuesta se retorna los datos de la misma y un código 201
    """

    try:
        
        complaint = complaint_schema.load(request.get_json())
        result = complaint_schema.dump(complaint)

        return jsonify(atributos=result), 201
        
    except (MarshmallowError, BadRequest):
        
        abort(400)

    except:
        
        abort(500)


@complaint_api.get("/")
def get():
    """
    Controller de la api para recuperar denuncias confirmadas (en curso, resueltas o cerradas).
    Se pagina en base a la configuración del sistema.

    @params:
        - pagina (int): número de página que se desea obtener (por defecto se envía la página 1)
    """

    try:

        if not validate_received_params(request.args):
            raise BadRequest

        page = request.args.get("pagina", None)

        page, per_page = validate_params_pagination(page)

        complaints = Complaint.all(page=page)

        complaints = paginated_complaints_schema.dump(complaints)

        return jsonify(complaints)

    except (BadRequest, ValueError):
        
        abort(400)

    except NotFound:

        abort(404, {"custom_description": 
                        "No se encontró la página solicitada"})

    except:

        abort(500)
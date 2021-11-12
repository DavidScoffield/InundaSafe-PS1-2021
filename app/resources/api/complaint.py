from flask import jsonify, Blueprint, request, abort
from app.models.complaint import Complaint
from app.schemas.complaint import complaint_schema
from marshmallow.exceptions import MarshmallowError

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
        
        json_data = complaint_schema.load(request.get_json())
        
    except MarshmallowError:
        
        abort(400)

    except:

        abort(500)

    else:

        complaint = Complaint.create_complaint(**json_data)
        result = complaint_schema.dump(complaint)

        return jsonify(atributos=result), 201
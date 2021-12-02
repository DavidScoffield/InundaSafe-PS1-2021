from flask import render_template, request, jsonify
from app.helpers.logger import logger_exception, logger_info


def get_description(e):
    description = None
    if (
        isinstance(e.description, dict)
        and "custom_description" in e.description.keys()
    ):
        description = e.description["custom_description"]

    return description


def bad_request_error(e):
    """
    Funcion helper para redirigir a una pagina error con
    un diccionario definido en caso de obtener un error 400
    """

    description = get_description(e)

    kwargs = {
        "error_name": "400 Bad Request",
        "error_description": "Por favor, verifique los datos ingresados"
        if description is None
        else description,
    }
    return make_response(kwargs, 400)


def not_found_error(e):
    """
    Funcion helper para redirigir a una pagina error
    con un diccionario definido en caso de obtener un error 404
    """
    description = get_description(e)

    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe"
        if description is None
        else description,
    }
    return make_response(kwargs, 404)


def unauthorized_error(e):
    """
    Funcion helper para redirigir a una pagina error con
    un diccionario definido en caso de obtener un error 401
    """
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return make_response(kwargs, 401)


def not_allowed_error(e):
    """
    Funcion helper para redirigir a una pagina error con
    un diccionario definido en caso de obtener un error 405
    """
    kwargs = {
        "error_name": "405 Method Not Allowed",
        "error_description": "No está permitido acceder a la url",
    }
    return make_response(kwargs, 405)


def internal_server_error(e):
    """
    Funcion helper para redirigir a una pagina error con
    un diccionario definido en caso de obtener un error 500
    """
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Ocurrió un error inesperado en el servidor",
    }
    return make_response(kwargs, 500)


def make_response(data, status):
    """
    Función que retorna el error en formato json en caso de que el requerimiento
    fuese de una api, o html en otro caso
    """
    if request.path.startswith("/api/"):
        return jsonify(data), status
    else:
        return render_template("error.html", **data), status

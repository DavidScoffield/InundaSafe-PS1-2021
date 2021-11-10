from flask import render_template, request, jsonify


def not_found_error(e):
    """
    Funcion helper para redirigir a una pagina error
    con un diccionario definido en caso de obtener un error 404
    """
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
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
        "error_description": "Ocurrió un error en el Servidor",
    }
    return make_response(kwargs, 500)


def make_response(data, status):
    if request.path.startswith("/api/"):
        return jsonify(data), status
    else:
        return render_template("error.html", **data), status

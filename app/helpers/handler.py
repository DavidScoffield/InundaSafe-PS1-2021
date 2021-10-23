from flask import render_template


def not_found_error(e):
    """
    Funcion helper para redirigir a una pagina error
    con un diccionario definido en caso de obtener un error 404
    """
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    """
    Funcion helper para redirigir a una pagina error con
    un diccionario definido en caso de obtener un error 401
    """
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return render_template("error.html", **kwargs), 401

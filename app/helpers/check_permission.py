from flask import session


def check_permission(permission):
    """
    Chequea que el permiso(String) pasado por parametro se
    encuentre en el listado de permisos almacenado en la sesion
    """
    return permission in session["permissions"]

from flask import (
    redirect,
    render_template,
    request,
    url_for,
    session,
    flash,
    Blueprint,
)
from app.models.user import User
from app.helpers.auth import authenticated

auth_routes = Blueprint(
    "auth_routes", __name__, url_prefix="/auth"
)


@auth_routes.get("/iniciar_sesion", endpoint="auth_login")
def login():
    "Controller para mostrar el formulario de login de la aplicacion"

    if authenticated(session):
        return redirect(url_for("home.index"))

    return render_template("auth/login.html")


@auth_routes.post(
    "/autenticacion", endpoint="auth_authenticate"
)
def authenticate():
    "Controller para autenticarse en la aplicacion"

    params = request.form
    email = params["email"]
    password = params["password"]

    if not email or not password:
        flash("Se deben completar todos los campos")
        return redirect(url_for("auth_routes.auth_login"))

    user = User.find_by_email_and_pass(email, password)

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_routes.auth_login"))

    if user.active == 0:
        flash("El usuario esta bloqueado")
        return redirect(url_for("auth_routes.auth_login"))

    permisos = []
    for rol in user.roles:
        for permiso in rol.permissions:
            permisos.append(permiso.name)
    permisos = set(permisos)

    session["user"] = user.id
    session["permissions"] = permisos
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home.index"))


@auth_routes.get("/cerrar_sesion", endpoint="auth_logout")
def logout():
    "Controller para manejar el cierre de sesion"
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_routes.auth_login"))

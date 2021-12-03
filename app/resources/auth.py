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
from app.helpers.forms.login_form import LoginForm
from app.resources.google_auth import auth_google_routes


auth_routes = Blueprint(
    "auth_routes", __name__, url_prefix="/auth"
)
# Google auth routes
auth_routes.register_blueprint(auth_google_routes)


@auth_routes.get("/iniciar_sesion", endpoint="auth_login")
def login():
    "Controller para mostrar el formulario de login de la aplicacion"

    if authenticated(session):
        return redirect(url_for("home.index"))

    form = LoginForm()

    return render_template("auth/login.html", form=form)

 
@auth_routes.post(
    "/autenticacion", endpoint="auth_authenticate"
)
def authenticate():
    "Controller para autenticarse en la aplicacion"

    params = request.form
    form = LoginForm(params)

    if not form.validate_on_submit():
        flash(
            "Por favor, corrija los errores",
            category="login_error",
        )
        return render_template("auth/login.html", form=form)
    else:
        args = form.data
        email = args["email"]
        password = args["password"]

        user = User.find_by_email_and_pass(email, password)

        if not user:
            flash(
                "Usuario o clave incorrecto.",
                category="login_error",
            )
            return redirect(
                url_for("auth_routes.auth_login")
            )

        if user.active == 0:
            flash(
                "El usuario esta bloqueado",
                category="login_error",
            )
            return redirect(
                url_for("auth_routes.auth_login")
            )

        if user.is_deleted:
            flash("El usuario fue eliminado",
                   category="login_error")
            return redirect(url_for("auth_routes.auth_login"))

        permisos = []
        for rol in user.roles:
            for permiso in rol.permissions:
                permisos.append(permiso.name)
        permisos = set(permisos)

        session["user"] = user.id
        session["permissions"] = permisos

    flash(
        "La sesión se inició correctamente.",
        category="login_succeful",
    )
    return redirect(url_for("home.index"))


@auth_routes.get("/cerrar_sesion", endpoint="auth_logout")
def logout():
    "Controller para manejar el cierre de sesion"
    del session["user"]
    session.clear()
    flash(
        "La sesión se cerró correctamente.",
        category="logout",
    )

    return redirect(url_for("auth_routes.auth_login"))

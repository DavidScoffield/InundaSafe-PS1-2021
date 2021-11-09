from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    session,
)
from app.helpers.auth import authenticated
from app.models.user import User

home = Blueprint("home", __name__, url_prefix="/")


@home.get("/")
def index():
    "Controller para mostrar la pagina de home de la aplicacion una vez logeado"

    if not authenticated(session):
        return redirect(url_for("auth_routes.auth_login"))

    return render_template("home.html")

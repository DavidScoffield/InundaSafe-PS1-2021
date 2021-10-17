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

    if not authenticated(session):
        return redirect(url_for("auth_routes.auth_login"))

    user_id = authenticated(session)
    user = User.find_user_by_id(user_id)

    return render_template("home.html", user=user)

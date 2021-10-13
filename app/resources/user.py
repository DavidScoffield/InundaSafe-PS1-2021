from flask import redirect, render_template, request, url_for, session, abort, Blueprint
#from app.db import connection
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission

user = Blueprint("user", __name__, url_prefix="/usuarios")

@user.route("/", methods=['GET'])
def index():
    if not authenticated(session):
        abort(401)

    if (not check_permission("usuario_index")):
        abort(401)

    users = User.find_all_users()

    #elimino al usuario del listado para que no se liste a él mismo
    this_user_id = session["user"]
    for user in users:
        if (user.id == this_user_id):
            users.remove(user)

    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)

    conn = connection()
    User.create(conn, request.form)
    return redirect(url_for("user_index"))

@user.route("/toggle_state/<int:user_id>/<state>", methods=['POST'])
def toggle_state(user_id, state):
    if not authenticated(session):
        abort(401)

    if (not check_permission("usuario_update")): #ojo con este permiso
        abort(401)

    # Si su estado era Activo (1), hay que ponerlo en 0 (Bloqueado). Si era Bloqueado hay que ponerlo en 1
    new_state = 0 if int(state)==1 else 1

    User.update_state(user_id, new_state)

    return redirect(url_for("user.index"))
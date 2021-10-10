from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    if (not check_permission("usuario_index")):
        abort(401)

    #conn = connection()
    #users = User.all(conn)
    users = User.find_all_users()

    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)

    #conn = connection()
    #User.create(conn, request.form)
    params = request.form

    user = User.check_existing_email_or_username(params["email"], params["username"])


    if user.email == params["email"]:
        flash("Ya existe un usuario con ese email")
        return redirect(url_for("user_new"))

    if user.username == params["username"]:
        flash("Ya existe un usuario con ese nombre de usuario")
        return redirect(url_for("user_new"))

        #ACA SE INSERTA AL USUARIO EN LA BD

    return redirect(url_for("user_index"))

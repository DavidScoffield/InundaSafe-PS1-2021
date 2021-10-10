from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
from app.models.role import Role
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
    params = request.form.to_dict()
    user = User.check_existing_email_or_username(params["email"], params["username"])

    if user:
        if user.email == params["email"]:
            flash("Ya existe un usuario con ese email")
            return redirect(url_for("user_new"))

        if user.username == params["username"]:
            flash("Ya existe un usuario con ese nombre de usuario")
            return redirect(url_for("user_new"))

    if params["state"] == "activo": #depende cual sea el estado pongo un int 1 o 0 para q quede acorde con bd
        params["state"] = 1
    else:
        params["state"] = 0
    
    new_user = User(params["email"], params["username"], params["password"], params["first_name"], params["last_name"], params["state"])
    User.insert_user(new_user)   #inserto al usuario en la bd

    roles = Role.find_roles_from_strings(request.form.getlist('rol')) #lista con los roles que va a tener el nuevo usuario
    Role.insert_rol(roles, new_user)  #inserto los roles en la tabla user_has_roles
     
    #FALTA VALIDAR CASOS BÁSICOS, COMO QUE NO SEA VACIO, ETC
    return redirect(url_for("user_index"))

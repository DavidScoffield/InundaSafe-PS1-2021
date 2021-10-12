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

    users = User.find_all_users()

    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)
    
    if (not check_permission("usuario_show")):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)
    
    if (not check_permission("usuario_new")):
        abort(401)

    params = request.form.to_dict()
    
    first_name = params["first_name"]
    last_name = params["last_name"]
    username = params["username"]
    email = params["email"]
    password = params["password"]
    state = request.form.get('state')
    selectedRoles = request.form.getlist('rol')

    if (not first_name or not last_name or not username or not email or not password or not state or not len(selectedRoles)):
        flash("Se deben completar todos los campos")
        return redirect(url_for("user_new"))

    user = User.check_existing_email_or_username(email, username)

    if user:
        if user.email == email:
            flash("Ya existe un usuario con ese email")
            return redirect(url_for("user_new"))

        if user.username == username:
            flash("Ya existe un usuario con ese nombre de usuario")
            return redirect(url_for("user_new"))

    if state == "activo": #depende cual sea el estado pongo un int 1 o 0 para q quede acorde con bd
        state = 1
    else:
        state = 0
    
    User.insert_user(email, username, password, first_name, last_name, state, selectedRoles)   #inserto al usuario en la bd
     
    return redirect(url_for("user_index"))

def toggle_state(user_id, state):
    if not authenticated(session):
        abort(401)

    if (not check_permission("usuario_update")): #ojo con este permiso
        abort(401)

    # Si su estado era Activo (1), hay que ponerlo en 0 (Bloqueado). Si era Bloqueado hay que ponerlo en 1
    new_state = 0 if int(state)==1 else 1

    User.update_state(user_id, new_state)

    return redirect(url_for("user_index"))
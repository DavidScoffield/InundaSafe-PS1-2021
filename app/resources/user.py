from flask import (
    redirect,
    render_template,
    request,
    url_for,
    session,
    abort,
    Blueprint,
    flash,
)
from app.models.user import User
from app.models.role import Role
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission

user = Blueprint("user", __name__, url_prefix="/usuarios")

#@user.route("/", methods=['GET'])
#def index():
#    if not authenticated(session):
#        abort(401)
#
#    if (not check_permission("usuario_index")):
#        abort(401)
#
#    users = User.find_all_users()
#
#    #elimino al usuario del listado para que no se liste a él mismo
#    this_user_id = session["user"]
#    for user in users:
#        if (user.id == this_user_id):
#            users.remove(user)
#
#    return render_template("user/index.html", users=users)

@user.get("/<int:page_number>")
def index(page_number):
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_index"):
        abort(401)

    users = User.paginate(page_number)

    #elimino al usuario del listado para que no se liste a él mismo
    this_user_id = session["user"]
    for user in users.items:
        if (user.id == this_user_id):
            users.items.remove(user)


    return render_template("user/index.html", users=users)


@user.get("/nuevo")
def new():
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_show"):
        abort(401)

    return render_template("user/new.html")


@user.post("/nuevo")
def create():
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_new"):
        abort(401)

    params = request.form.to_dict()

    first_name = params["first_name"]
    last_name = params["last_name"]
    username = params["username"]
    email = params["email"]
    password = params["password"]
    state = request.form.get("state")
    selectedRoles = request.form.getlist("rol")

    if (
        not first_name
        or not last_name
        or not username
        or not email
        or not password
        or not state
        or not len(selectedRoles)
    ):
        flash("Se deben completar todos los campos")
        return redirect(url_for("user.new"))

    user = User.check_existing_email_or_username(email, username)

    if user:
        if user.email == email:
            flash("Ya existe un usuario con ese email")
            return redirect(url_for("user.new"))

        if user.username == username:
            flash("Ya existe un usuario con ese nombre de usuario")
            return redirect(url_for("user.new"))

    if (
        state == "activo"
    ):  # depende cual sea el estado pongo un int 1 o 0 para q quede acorde con bd
        state = 1
    else:
        state = 0
    
    User.insert_user(email, username, password, first_name, last_name, state, selectedRoles)   #inserto al usuario en la bd
     
    return redirect(url_for("user.index", page_number=1))


@user.route("/toggle_state/<int:user_id>/<state>", methods=["POST"])
def toggle_state(user_id, state):
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_update"):  # ojo con este permiso
        abort(401)

    # Si su estado era Activo (1), hay que ponerlo en 0 (Bloqueado). Si era Bloqueado hay que ponerlo en 1
    new_state = 0 if int(state) == 1 else 1

    User.update_state(user_id, new_state)

    return redirect(url_for("user.index", page_number=1))

@user.post("/editar")
def delete():
    if not authenticated(session) or not check_permission("usuario_destroy"):
        abort(401)


    User.delete_user(request.form["user_id"])
    return redirect(url_for("user.index", page_number=1))

@user.get("/editar/<int:user_id>")
def edit(user_id):
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_show"):  # es este permiso????????'
        abort(401)

    user = User.find_user_by_id(user_id)
    return render_template("user/edit_other_user.html", user=user)

@user.post("/editar/<int:user_id>")
def update(user_id):
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_update"):  # ojo con este permiso
        abort(401)

    params = request.form.to_dict()
    first_name = params["first_name"]
    last_name = params["last_name"]
    email = params["email"]
    password = params["password"]
    state = request.form.get("state")
    selectedRoles = request.form.getlist("rol")
    
    if (
        not first_name
        or not last_name
        or not email
        or not password
        or not state
        or not len(selectedRoles)
    ):
        flash("Se deben completar todos los campos")
        return redirect(url_for("user.edit", user_id=user_id))

    user_email = User.check_existing_email_with_different_id(email, user_id)
    if user_email:
        if user_email.email == email:
            flash("Ya existe un usuario con ese email")
            return redirect(url_for("user.edit", user_id=user_id))

    User.update_user(user_id, params, selectedRoles)
    
    return redirect(url_for("user.edit", user_id=user_id))

@user.get("/miPerfil")
def edit_my_profile():
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_show"):
        abort(401)
    
    user = User.find_user_by_id(session['user'])

    return render_template("user/my_profile.html", user=user)

@user.post("/miPerfil")
def update_my_profile():
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_update"):  # ojo con este permiso
        abort(401)

  
    return redirect(url_for("user.edit_my_profile"))
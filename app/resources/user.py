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
from app.helpers.has_role import has_role

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


@user.post("/toggle_state")
def toggle_state():
    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_update"):  # ojo con este permiso
        abort(401)

    user_id = request.form["user_id"]
    state = request.form["state"]

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

    #este if está por si dos admins se intentan sacar el permiso de admin mutuamente al mismo tiempo
    roles = Role.find_roles_from_strings(selectedRoles) 
    if not has_role(roles, "rol_administrador"): #si NO está chequeado el admin, entonces
        all_users = User.find_all_users() #busco a todos los usuarios
        lista = []
        for u in all_users:
            for r in u.roles:
                lista.append(r.name) #y armo una lista con todos los roles de todos los usuarios
        if (lista.count("rol_administrador") <= 1): #si hay 1 admin entonces no es posible dejar de ser admin porque no puede dejar de haber
            flash("No puede dejar de ser administrador ya que usted es el único existente")
            return redirect(url_for("user.edit_my_profile"))

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
    
    params = request.form.to_dict()
    first_name = params["first_name"]
    last_name = params["last_name"]
    email = params["email"]
    password = params["password"]
    state = request.form.get("state")
    selectedRoles = request.form.getlist("rol")

    user = User.find_user_by_id(session['user'])
    isAdmin = has_role(user.roles, "rol_administrador")
    if isAdmin:
        roles = Role.find_roles_from_strings(selectedRoles) 
        if not has_role(roles, "rol_administrador"): #si NO está chequeado el admin, entonces
            all_users = User.find_all_users() #busco a todos los usuarios
            lista = []
            for u in all_users:
                for r in u.roles:
                    lista.append(r.name) #y armo una lista con todos los roles de todos los usuarios
            if (lista.count("rol_administrador") <= 1): #si hay 1 admin entonces no es posible dejar de ser admin porque no puede dejar de haber
                flash("No puede dejar de ser administrador ya que usted es el único existente")
                return redirect(url_for("user.edit_my_profile"))

        if (
            not first_name
            or not last_name
            or not email
            or not password
            or not state
            or not len(selectedRoles)
        ):
            flash("Se deben completar todos los campos")
            return redirect(url_for("user.edit_my_profile"))
    else:
        if (
            not first_name
            or not last_name
            or not email
            or not password
        ):
            flash("Se deben completar todos los campos")
            return redirect(url_for("user.edit_my_profile"))
    
    user_email = User.check_existing_email_with_different_id(email, user.id)
    if user_email:
        if user_email.email == email:
            flash("Ya existe un usuario con ese email")
            return redirect(url_for("user.edit_my_profile"))
    
    User.update_profile(user, params, selectedRoles, isAdmin)

  
    return redirect(url_for("user.edit_my_profile"))
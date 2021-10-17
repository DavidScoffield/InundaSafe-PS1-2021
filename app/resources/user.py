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
from app.helpers.check_param_search import (
    active_dic,
    check_param,
)

from app.helpers.forms.new_user_form import NewUserForm

user = Blueprint("user", __name__, url_prefix="/usuarios")


@user.get("/<int:page_number>")
def index(page_number):
    """
    Controller para mostrar el listado de usuarios
    Recibe como parametro el numero de la pagina a mostrar
    Puede recibir como argumentos:
    - name : string -> campo de filtro para los nombres de usuarios
    - active : string -> campo de filtro para los estados(activado, desactivado) de usuarios
    """

    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_index"):
        abort(401)

    args = request.args
    name = args.get("name")
    active = args.get("active")

    name = check_param("@user/name", name)
    active = check_param("@user/active", active_dic(active))

    # Busco los usuarios con sus filtros correspondientes
    users = User.search(
        active=active,
        name=name,
        dont_use_active=type(active) is not int,
    )
    # elimino al usuario del listado para que no se liste a él mismo
    this_user_id = session["user"]
    users = User.exclude_user(users, this_user_id)

    paginated_users = User.paginate(
        page_number=page_number,
        users=users,
    )

    # En caso que no encuentre ningun resultado se redirige a la pagina 1 con los argumentos de busqueda
    if (
        paginated_users.page != 1
        and paginated_users.page > paginated_users.pages
    ):
        # Si la cantidad de paginas es 0, se redirigira a la pagina 1
        if paginated_users.pages > 0:
            page = paginated_users.pages
        else:
            page = 1

        return redirect(
            url_for(
                "user.index",
                page_number=page,
                **request.args
            )
        )

    return render_template(
        "user/index.html", users=paginated_users
    )


@user.get("/nuevo")
def new():
    "Controller para mostrar el formulario para el alta de un usuario"

    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_show"):
        abort(401)

    form = NewUserForm()

    return render_template("user/new.html", form=form)


@user.post("/nuevo")
def create():
    "Controller para crear un usuario en base a los datos enviados en el formulario"

    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_new"):
        abort(401)

    form = NewUserForm(request.form)

    params = form.data

    first_name = params["first_name"]
    last_name = params["last_name"]
    username = params["username"]
    email = params["email"]
    password = params["password"]
    state = request.form.get("state")
    # selectedRoles = request.form.getlist("rol")

    selectedRoles = []

    # genero una lista de strings con los roles seleccionados en el form
    for rol in ["rol_administrador", "rol_operador"]:
        if params[rol]:
            selectedRoles += [rol]

    # validaciones back: validate_on_submit() llama a los validators.DataRequired() de todos los campos (chequea que no esten vacios) y llama
    # ademas al validador custom validate_rol_label() definido en la clase que chequea que se haya clickeado al menos un checkbox.
    if not form.validate_on_submit():
        flash("Por favor, corrija los errores")
        return render_template("user/new.html", form=form)
    else:
        user = User.check_existing_email_or_username(
            email, username
        )

        if user:
            if user.email == email:
                flash("Ya existe un usuario con ese email")
                return redirect(url_for("user.new"))

            if user.username == username:
                flash(
                    "Ya existe un usuario con ese nombre de usuario"
                )
                return redirect(url_for("user.new"))
        if (
            state == "activo"
        ):  # depende cual sea el estado pongo un int 1 o 0 para q quede acorde con bd
            state = 1
        else:
            state = 0

        User.insert_user(
            email,
            username,
            password,
            first_name,
            last_name,
            state,
            selectedRoles,
        )  # inserto al usuario en la bd

    flash("Usuario creado correctamente")
    return redirect(url_for("user.index", page_number=1))


@user.post("/toggle_state")
def toggle_state():
    "Controller para menejar el cambio de estado de un usuario"

    if not authenticated(session):
        abort(401)

    if not check_permission(
        "usuario_update"
    ):  # ojo con este permiso
        abort(401)

    user_id = request.form["user_id"]
    state = request.form["state"]

    # Si su estado era Activo (1), hay que ponerlo en 0 (Bloqueado). Si era Bloqueado hay que ponerlo en 1
    new_state = 0 if int(state) == 1 else 1

    User.update_state(user_id, new_state)

    return redirect(url_for("user.index", page_number=1))


@user.post("/editar")
def delete():
    "Controller para eliminar un usuario"

    if not authenticated(session) or not check_permission(
        "usuario_destroy"
    ):
        abort(401)

    User.delete_user(request.form["user_id"])
    return redirect(url_for("user.index", page_number=1))


@user.get("/editar/<int:user_id>")
def edit(user_id):
    "Controller para mostrar el formulario para la edicion de un usuario"

    if not authenticated(session):
        abort(401)

    if not check_permission(
        "usuario_show"
    ):  # es este permiso????????'
        abort(401)

    user = User.find_user_by_id(user_id)
    return render_template(
        "user/edit_other_user.html", user=user
    )


@user.post("/editar/<int:user_id>")
def update(user_id):
    "Controller para editar un usuario en base a los datos del formulario"

    if not authenticated(session):
        abort(401)

    if not check_permission(
        "usuario_update"
    ):  # ojo con este permiso
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
        return redirect(
            url_for("user.edit", user_id=user_id)
        )

    # este if está por si dos admins se intentan sacar el permiso de admin mutuamente al mismo tiempo
    roles = Role.find_roles_from_strings(selectedRoles)

    user = User.find_user_by_id(user_id)
    user_was_admin = False
    for rol in user.roles:
        if rol.name == "rol_administrador":
            user_was_admin = True

    if (
        not has_role(roles, "rol_administrador")
        and user_was_admin
    ):  # si NO está chequeado el admin, entonces
        all_users = (
            User.find_all_users()
        )  # busco a todos los usuarios
        lista = []
        for u in all_users:
            for r in u.roles:
                lista.append(
                    r.name
                )  # y armo una lista con todos los roles de todos los usuarios
        if (
            lista.count("rol_administrador") <= 1
        ):  # si hay 1 admin entonces no es posible dejar de ser admin porque no puede dejar de haber
            flash(
                "No puede dejar de ser administrador ya que usted es el único existente"
            )
            return redirect(
                url_for("user.edit", user_id=user_id)
            )

    user_email = (
        User.check_existing_email_with_different_id(
            email, user_id
        )
    )
    if user_email:
        if user_email.email == email:
            flash("Ya existe un usuario con ese email")
            return redirect(
                url_for("user.edit", user_id=user_id)
            )

    User.update_user(user_id, params, selectedRoles)

    return redirect(url_for("user.edit", user_id=user_id))


@user.get("/miPerfil")
def edit_my_profile():
    "Controller para mostrar el formulario de edicion de perfil para el usuario logeado"

    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_show"):
        abort(401)

    user = User.find_user_by_id(session["user"])

    return render_template(
        "user/my_profile.html", user=user
    )


@user.post("/miPerfil")
def update_my_profile():
    "Controller para editar el perfil del usuario logeado"

    if not authenticated(session):
        abort(401)

    if not check_permission(
        "usuario_update"
    ):  # ojo con este permiso
        abort(401)

    params = request.form.to_dict()
    first_name = params["first_name"]
    last_name = params["last_name"]
    email = params["email"]
    password = params["password"]
    state = request.form.get("state")
    selectedRoles = request.form.getlist("rol")

    user = User.find_user_by_id(session["user"])
    isAdmin = has_role(user.roles, "rol_administrador")
    if isAdmin:
        roles = Role.find_roles_from_strings(selectedRoles)
        if not has_role(
            roles, "rol_administrador"
        ):  # si NO está chequeado el admin, entonces
            all_users = (
                User.find_all_users()
            )  # busco a todos los usuarios
            lista = []
            for u in all_users:
                for r in u.roles:
                    lista.append(
                        r.name
                    )  # y armo una lista con todos los roles de todos los usuarios
            if (
                lista.count("rol_administrador") <= 1
            ):  # si hay 1 admin entonces no es posible dejar de ser admin porque no puede dejar de haber
                flash(
                    "No puede dejar de ser administrador ya que usted es el único existente"
                )
                return redirect(
                    url_for("user.edit_my_profile")
                )

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

    user_email = (
        User.check_existing_email_with_different_id(
            email, user.id
        )
    )
    if user_email:
        if user_email.email == email:
            flash("Ya existe un usuario con ese email")
            return redirect(url_for("user.edit_my_profile"))

    User.update_profile(
        user, params, selectedRoles, isAdmin
    )

    return redirect(url_for("user.edit_my_profile"))

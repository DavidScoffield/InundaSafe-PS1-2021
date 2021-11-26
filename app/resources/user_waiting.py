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
from app.models.user_waiting import UserWaiting
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission
from app.helpers.has_role import has_role
from app.helpers.check_param_search import (
    active_dic,
    check_param,
)

from app.helpers.forms.new_user_form import NewUserForm
from app.helpers.forms.edit_other_user_form import (
    EditOtherUserForm,
)
from app.helpers.forms.edit_my_profile_form import (
    EditMyProfileForm,
)

user_waiting = Blueprint(
    "user_waiting",
    __name__,
    url_prefix="/usuarios-aprobacion",
)


@user_waiting.get("/<int:page_number>")
def index(page_number):
    """
    Controller para mostrar el listado de usuarios en espera de aprobacion
    Recibe como parametro el numero de la pagina a mostrar
    Puede recibir como argumentos:
    - email : string -> campo de filtro para los emails
    """

    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_waiting_index"):
        abort(401)

    args = request.args
    email = args.get("email")

    email = check_param("@user_waiting/email", email)

    # Busco los usuarios con sus filtros correspondientes
    paginated_users = UserWaiting.search_paginate(
        email=email,
        page_number=page_number,
    )

    if paginated_users.total == 0:
        flash(
            "No se encontraron resultados",
            category="user_waiting_index",
        )
        found_users = False
    else:
        found_users = True

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
                "user_waiting.index",
                page_number=page,
                **request.args
            )
        )

    return render_template(
        "user_waiting/index.html",
        users=paginated_users,
        found_users=found_users,
    )


# @user_waiting.get("/nuevo")
# def new():
#     "Controller para mostrar el formulario para el alta de un usuario"

#     if not authenticated(session):
#         abort(401)

#     if not check_permission("usuario_show"):
#         abort(401)

#     form = NewUserForm()

#     return render_template("user/new.html", form=form)


# @user_waiting.post("/nuevo")
# def create():
#     "Controller para crear un usuario en base a los datos enviados en el formulario"

#     if not authenticated(session):
#         abort(401)

#     if not check_permission("usuario_new"):
#         abort(401)

#     form = NewUserForm(request.form)

#     params = form.data

#     first_name = params["first_name"]
#     last_name = params["last_name"]
#     username = params["username"]
#     email = params["email"]
#     password = params["password"]
#     state = request.form.get("active")
#     # selectedRoles = request.form.getlist("rol")

#     selectedRoles = []

#     # genero una lista de strings con los roles seleccionados en el form
#     for rol in ["rol_administrador", "rol_operador"]:
#         if params[rol]:
#             selectedRoles += [rol]

#     # validaciones back: validate_on_submit() llama a los validators.DataRequired()
#     # de todos los campos (chequea que no esten vacios) y llama ademas al validador
#     # custom validate_rol_label() definido en la clase que chequea que se haya clickeado
#     # al menos un checkbox.
#     if not form.validate_on_submit():
#         flash(
#             "Por favor, corrija los errores",
#             category="user_create",
#         )
#         return render_template("user/new.html", form=form)
#     else:
#         user = User.check_existing_email_or_username(
#             email, username
#         )

#         if user:
#             if user.email == email:
#                 flash(
#                     "Ya existe un usuario con ese email",
#                     category="user_create",
#                 )
#                 return redirect(url_for("user.new"))

#             if user.username == username:
#                 flash(
#                     "Ya existe un usuario con ese nombre de usuario",
#                     category="user_create",
#                 )
#                 return redirect(url_for("user.new"))

#         # Chequear que el email no este en la tabla de usuarios en espera
#         user_waiting = UserWaiting.check_existing_email(
#             email
#         )

#         if user_waiting:
#             flash(
#                 "Ya existe un usuario con ese email",
#                 category="user_create",
#             )
#             return redirect(url_for("user.new"))

#         if (
#             state == "activo"
#         ):  # depende cual sea el estado pongo un int 1 o 0 para q quede acorde con bd
#             state = 1
#         else:
#             state = 0

#         # Si esta creando a un admin, lo seteo como Activo, para que no pueda crearlo Bloqueado
#         if "rol_administrador" in selectedRoles:
#             state = 1

#         User.insert_user(
#             email,
#             username,
#             password,
#             first_name,
#             last_name,
#             state,
#             selectedRoles,
#         )  # inserto al usuario en la bd

#     flash(
#         "Usuario creado correctamente",
#         category="user_create",
#     )
#     return redirect(url_for("user.index", page_number=1))


# @user_waiting.post("/toggle_state")
# def toggle_state():
#     "Controller para menejar el cambio de estado de un usuario"

#     if not authenticated(session):
#         abort(401)

#     if not check_permission("usuario_update"):
#         abort(401)

#     user_id = request.form["user_id"]
#     state = request.form["state"]

#     # Si su estado era Activo (1), hay que ponerlo en 0 (Bloqueado). Si era Bloqueado hay que ponerlo en 1
#     new_state = 0 if int(state) == 1 else 1

#     User.update_state(user_id, new_state)

#     return redirect(url_for("user.index", page_number=1))


# @user_waiting.post("/editar")
# def delete():
#     "Controller para eliminar un usuario"

#     if not authenticated(session) or not check_permission(
#         "usuario_destroy"
#     ):
#         abort(401)

#     User.delete_user(request.form["user_id"])
#     return redirect(url_for("user.index", page_number=1))


@user_waiting.get("/administrar/<int:user_id>")
def manage(user_id):
    """
    Controller para mostrar el formulario para la aprobacion o rechazo
    de un usuario
    """

    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_waiting_manage"):
        abort(401)

    user = UserWaiting.find_user_by_id(user_id)

    # Si intenta acceder por URL con un id que no existe o que esta eliminado aborta.
    if not user:
        abort(404)

    form = EditOtherUserForm(**user.get_attributes())

    return render_template(
        "user_waiting/manage.html",
        user=user,
        form=form,
    )


# @user_waiting.post("/editar/<int:user_id>")
# def update(user_id):
#     "Controller para editar un usuario en base a los datos del formulario"

#     if not authenticated(session):
#         abort(401)

#     if not check_permission("usuario_update"):
#         abort(401)

#     form = EditOtherUserForm(request.form)

#     params = form.data

#     email = params["email"]

#     selectedRoles = []
#     # genero una lista de strings con los roles seleccionados en el form
#     for rol in ["rol_administrador", "rol_operador"]:
#         if params[rol]:
#             selectedRoles += [rol]

#     user = User.find_user_by_id(user_id)
#     if (
#         not form.validate_on_submit()
#     ):  # validaciones del back WTF
#         flash(
#             "Por favor, corrija los errores",
#             category="update_user",
#         )
#         return render_template(
#             "user/edit_other_user.html",
#             user=user,
#             form=form,
#         )

#     # este if está por si dos admins se intentan sacar el permiso de admin mutuamente al mismo tiempo
#     roles = Role.find_roles_from_strings(selectedRoles)

#     user = User.find_user_by_id(user_id)
#     user_was_admin = False
#     for rol in user.roles:
#         if rol.name == "rol_administrador":
#             user_was_admin = True

#     # Por si se deshabilita el chequeo del front e intenta bloquear a un Admin al editarlo
#     if user_was_admin:
#         params["active"] = "activo"

#     update_password = True
#     # Si la contraseña se envia vacia, no la queria editar: La dejo como estaba en la BD
#     if not params["password"]:
#         update_password = False

#     if (
#         not has_role(roles, "rol_administrador")
#         and user_was_admin
#     ):  # si NO está chequeado el admin, entonces
#         all_users = (
#             User.find_all_users()
#         )  # busco a todos los usuarios
#         lista = []
#         for u in all_users:
#             for r in u.roles:
#                 lista.append(
#                     r.name
#                 )  # y armo una lista con todos los roles de todos los usuarios
#         if (
#             lista.count("rol_administrador") <= 1
#         ):  # si hay 1 admin entonces no es posible dejar de ser admin porque no puede dejar de haber
#             flash(
#                 "No puede dejar de ser administrador ya que usted es el único existente",
#                 category="update_user",
#             )
#             return redirect(
#                 url_for("user.edit", user_id=user_id)
#             )

#     user_email = (
#         User.check_existing_email_with_different_id(
#             email, user_id
#         )
#     )
#     if user_email:
#         if user_email.email == email:
#             flash(
#                 "Ya existe un usuario con ese email",
#                 category="update_user",
#             )
#             return redirect(
#                 url_for("user.edit", user_id=user_id)
#             )

#     User.update_user(
#         user_id, params, selectedRoles, update_password
#     )
#     flash(
#         "Usuario editado correctamente",
#         category="update_user",
#     )

#     return redirect(url_for("user.edit", user_id=user_id))


# @user_waiting.get("/miPerfil")
# def edit_my_profile():
#     "Controller para mostrar el formulario de edicion de perfil para el usuario logeado"

#     if not authenticated(session):
#         abort(401)

#     if not check_permission("usuario_show_my_profile"):
#         abort(401)

#     user = User.find_user_by_id(session["user"])

#     form = EditMyProfileForm(**user.get_attributes())

#     return render_template(
#         "user/my_profile.html", user=user, form=form
#     )


# @user_waiting.post("/miPerfil")
# def update_my_profile():
#     "Controller para editar el perfil del usuario logeado"

#     if not authenticated(session):
#         abort(401)

#     if not check_permission("usuario_update_my_profile"):
#         abort(401)

#     form = EditMyProfileForm(request.form)

#     params = form.data

#     selectedRoles = []
#     # genero una lista de strings con los roles seleccionados en el form
#     for rol in ["rol_administrador", "rol_operador"]:
#         if params[rol]:
#             selectedRoles += [rol]

#     user = User.find_user_by_id(session["user"])

#     if (
#         not form.validate_on_submit()
#     ):  # validaciones del back WTF
#         flash(
#             "Por favor, corrija los errores",
#             category="user_my_profile",
#         )
#         return render_template(
#             "user/my_profile.html", user=user, form=form
#         )

#     email = params["email"]

#     update_password = True
#     # Si la contraseña se envia vacia, no la queria editar: La dejo como estaba en la BD
#     if not params["password"]:
#         update_password = False

#     isAdmin = has_role(user.roles, "rol_administrador")
#     if isAdmin:
#         roles = Role.find_roles_from_strings(selectedRoles)
#         if not has_role(
#             roles, "rol_administrador"
#         ):  # si NO está chequeado el admin, entonces
#             all_users = (
#                 User.find_all_users()
#             )  # busco a todos los usuarios
#             lista = []
#             for u in all_users:
#                 for r in u.roles:
#                     lista.append(
#                         r.name
#                     )  # y armo una lista con todos los roles de todos los usuarios
#             if (
#                 lista.count("rol_administrador") <= 1
#             ):  # si hay 1 admin entonces no es posible dejar de ser admin porque no puede dejar de haber
#                 flash(
#                     "No puede dejar de ser administrador ya que usted es el único existente",
#                     category="user_my_profile",
#                 )
#                 return redirect(
#                     url_for("user.edit_my_profile")
#                 )

#     user_email = (
#         User.check_existing_email_with_different_id(
#             email, user.id
#         )
#     )
#     if user_email:
#         flash(
#             "Ya existe un usuario con ese email",
#             category="user_my_profile",
#         )
#         return redirect(url_for("user.edit_my_profile"))

#     User.update_profile(
#         user,
#         params,
#         selectedRoles,
#         isAdmin,
#         update_password,
#     )
#     flash(
#         "Perfil actualizado correctamente",
#         category="user_my_profile",
#     )

#     return redirect(url_for("user.edit_my_profile"))


# @user_waiting.post("/show")
# def show():
#     "Controller para mostrar la información de un usuario"

#     if not authenticated(session) or not check_permission(
#         "usuario_show"
#     ):
#         abort(401)

#     id_user = request.form["id_user"]
#     user = User.find_user_by_id_not_deleted(id_user)
#     if not user:
#         # flash(
#         #     "No se encontró el usuario especificado",
#         #     category="user_show",
#         # )
#         # return redirect(
#         #     url_for("user.index", page_number=1)
#         # )
#         abort(404)

#     return render_template(
#         "user/show.html",
#         user=user,
#     )

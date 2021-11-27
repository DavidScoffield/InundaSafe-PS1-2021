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
from app.models.user_waiting import UserWaiting
from app.helpers.auth import authenticated
from app.helpers.check_permission import check_permission
from app.helpers.check_param_search import (
    check_param,
)

from app.helpers.forms.approve_user import ApproveUserForm

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


@user_waiting.post("/rechazar")
def refuse():
    "Controller para rechazar la solicitud de aprobacion de un usuario"

    if not authenticated(session) or not check_permission(
        "usuario_waiting_refuse"
    ):
        abort(401)

    user = UserWaiting.find_user_by_id(
        request.form["user_id"]
    )

    if not user:
        abort(404)

    user.delete()

    return redirect(
        url_for("user_waiting.index", page_number=1)
    )


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

    form = ApproveUserForm(**user.get_attributes())

    return render_template(
        "user_waiting/manage.html",
        user=user,
        form=form,
    )


@user_waiting.post("/aprobar/<int:user_id>")
def approve(user_id):
    "Controller para aprobar un usuario"

    if not authenticated(session):
        abort(401)

    if not check_permission("usuario_waiting_approve"):
        abort(401)

    form = ApproveUserForm(request.form)
    params = form.data

    username = params["suggested_username"]
    state = request.form.get("active")

    selectedRoles = []
    # genero una lista de strings con los roles seleccionados en el form
    for rol in ["rol_administrador", "rol_operador"]:
        if params[rol]:
            selectedRoles += [rol]

    # validaciones back: validate_on_submit() llama a los validators.DataRequired()
    # de todos los campos (chequea que no esten vacios) y llama ademas al validador
    # custom validate_rol_label() definido en la clase que chequea que se haya clickeado
    # al menos un checkbox.
    if not form.validate_on_submit():
        user = UserWaiting.find_user_by_id(user_id)
        flash(
            "Por favor, corrija los errores",
            category="user_waiting_manage",
        )
        return render_template(
            "user_waiting/manage.html", form=form, user=user
        )
    else:
        # Comprobar unicidad nombre de usuario
        user = User.check_existing_email_or_username(
            username=username
        )

        if user:
            flash(
                "Ya existe un usuario con ese nombre de usuario",
                category="user_waiting_manage",
            )

            return render_template(
                "user_waiting/manage.html",
                user=user,
                form=form,
            )

        # depende cual sea el estado pongo un int 1 o 0 para q quede
        # acorde con bd
        state = 1 if state == "activo" else 0

        # Si esta habilitando a un admin, lo seteo como Activo, para que no
        # pueda habilitarlo Bloqueado
        if "rol_administrador" in selectedRoles:
            state = 1

        # Juntar datos finales
        user = UserWaiting.find_user_by_id(user_id)

        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        password = "RegistradoConRedSocial123"

        User.insert_user(
            email,
            username,
            password,
            first_name,
            last_name,
            state,
            selectedRoles,
        )  # inserto al usuario en la bd

        # Eliminar user de tabla de users_waiting
        user.delete()

    flash(
        "Usuario habilitado en el sistema correctamente",
        category="user_waiting_approve",
    )
    return redirect(
        url_for("user_waiting.index", page_number=1)
    )

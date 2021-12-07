import json
import requests
from flask import (
    redirect,
    render_template,
    request,
    url_for,
    abort,
    session,
    flash,
    Flask,
    Blueprint,
    current_app,
)

# from app.db import connection
from app.models.user import User
from app.models.user_waiting import UserWaiting
from app.helpers.auth import get_google_provider_cfg

from oauthlib.oauth2 import WebApplicationClient

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app.helpers.logger import logger_info

auth_google_routes = Blueprint(
    "auth_google_routes",
    __name__,
    url_prefix="/google",
)


# ---- LOGIN
@auth_google_routes.get("/iniciar_sesion")
def login():
    """
    Controller para la redireccion a la pagina para logearse con google
    """
    request_uri = use_auth_google(
        redirect_uri="REDIRECT_LOGIN_URI_GOOGLE"
    )
    return redirect(request_uri)


@auth_google_routes.get("/iniciar_sesion/callback")
def callback_login():
    """
    - Controller para manejar el callback del inicio de sesion con Google.
    - Verifica los datos devueltos y logea al usuario o informa reportes
    dependiendo las condiciones del sistema en base a los datos recuperados
    """
    userinfo_response = callback_auth_google(request)

    # Comprobar si ya esta registrado el usuario
    user_logged = User.find_by_email_for_social_media(
        email=userinfo_response["email"]
    )

    if not user_logged:
        # Comprobar si ya a la espera de aprobación
        user_with_email = UserWaiting.check_existing_email(
            email=userinfo_response["email"]
        )

        if user_with_email:
            flash(
                "No está registrado, pero se encuentra a la espera de aprobación de un administrador. Inténtelo mas tarde!",
                category="auth_google_login",
            )
        else:
            flash(
                "Debe registrarse para poder iniciar sesión",
                category="auth_google_login",
            )
        return redirect(url_for("auth_routes.auth_login"))

    # Iniciar sesion

    if user_logged.active == 0:
        flash(
            "El usuario esta bloqueado",
            category="auth_google_login",
        )
        return redirect(url_for("auth_routes.auth_login"))

    if user.is_deleted:
            flash("El usuario fue eliminado",
                   category="login_error")
            return redirect(url_for("auth_routes.auth_login"))

    permisos = []
    for rol in user_logged.roles:
        for permiso in rol.permissions:
            permisos.append(permiso.name)
    permisos = set(permisos)

    session["user"] = user_logged.id
    session["permissions"] = permisos

    flash(
        "La sesión se inició correctamente.",
        category="login_succeful",
    )
    return redirect(url_for("home.index"))


# -----------

# ---- REGISTER
@auth_google_routes.get("/registro")
def register():
    """
    Controller para la redireccion a la pagina para registrarse con google
    """
    request_uri = use_auth_google(
        redirect_uri="REDIRECT_REGISTER_URI_GOOGLE"
    )
    return redirect(request_uri)


@auth_google_routes.get("/registro/callback")
def callback_register():
    """
    - Controller para manejar el callback del registro con Google.
    - Verifica los datos devueltos y regitra al usuario o informa reportes
    dependiendo las condiciones del sistema en base a los datos recuperados
    """
    userinfo_response = callback_auth_google(request)

    # Comprobar si ya esta registrado el usuario
    user_logged = User.check_existing_email_or_username(
        email=userinfo_response["email"]
    )

    if user_logged:
        if user_logged.created_by_social_media == 1:
            flash(
                "Ya está registrado con este usuario, intente iniciando sesión!",
                category="auth_google_register",
            )
        else:
            flash(
                "El email con el que quiere registrarse ya está en uso en el sistema, intente con otra cuenta.",
                category="auth_google_register",
            )
        return redirect(url_for("auth_routes.auth_login"))

    # Comprobar si ya a la espera de aprobación
    user_with_email = UserWaiting.check_existing_email(
        email=userinfo_response["email"]
    )

    if user_with_email:
        flash(
            "Ya se encuentra a la espera de aprobación de un administrador!",
            category="auth_google_register",
        )
        return redirect(url_for("auth_routes.auth_login"))

    email = userinfo_response["email"]
    first_name = userinfo_response["given_name"]
    last_name = userinfo_response["family_name"]
    suggested_username = f"{userinfo_response['given_name']}{userinfo_response['family_name']}"

    # Se guarda los datos del usuario para esperar aprobacion
    UserWaiting.new(
        email, suggested_username, first_name, last_name
    )

    flash(
        "¡Su solicitud de aprobación fue existosamente enviada, cuando un administrador lo habilite podrá comenzar a utilizar el sistema!",
        category="auth_google_register",
    )

    return redirect(url_for("auth_routes.auth_login"))


# -----------


def use_auth_google(redirect_uri: str):
    client = current_app.client
    REDIRECT_URI_GOOGLE = current_app.config[redirect_uri]

    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg[
        "authorization_endpoint"
    ]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=REDIRECT_URI_GOOGLE,
        scope=["openid", "email", "profile"],
    )

    return request_uri


def callback_auth_google(request):
    client = current_app.client
    GOOGLE_CLIENT_ID = current_app.config[
        "GOOGLE_CLIENT_ID"
    ]
    GOOGLE_CLIENT_SECRET = current_app.config[
        "GOOGLE_CLIENT_SECRET"
    ]

    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    (
        token_url,
        headers,
        body,
    ) = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(
        json.dumps(token_response.json())
    )

    userinfo_endpoint = google_provider_cfg[
        "userinfo_endpoint"
    ]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(
        uri, headers=headers, data=body
    )
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        abort(
            400,
            {
                "custom_description": "El email del usuario no esta disponible o no ha sido verificado por Google.",
            },
        )

    # Chequeo de existencia de usuario
    # stored_user = User

    # # Create a user in your db with the information provided
    # # by Google
    # user = User(
    #     id_=unique_id,
    #     name=users_name,
    #     email=users_email,
    #     profile_pic=picture,
    # )

    # # Doesn't exist? Add it to the database.
    # print(userinfo_response.json())
    # if not User.get(unique_id):
    #     User.create(
    #         unique_id, users_name, users_email, picture
    #     )

    # Begin user session by logging the user in
    # login_user(user)
    return userinfo_response.json()


@auth_google_routes.get("/bienvenido")
def bienvenido():
    return render_template("auth/bienvenido.html")


@auth_google_routes.get("/cerrar_sesion_google")
def logout():
    logout_user()
    return redirect(url_for("index"))

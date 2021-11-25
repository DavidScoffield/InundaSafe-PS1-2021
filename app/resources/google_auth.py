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


# client = WebApplicationClient(GOOGLE_CLIENT_ID)


@auth_google_routes.get("/")
def login():
    client = current_app.client
    REDIRECT_URI_GOOGLE = current_app.config[
        "REDIRECT_URI_GOOGLE"
    ]

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
    return redirect(request_uri)


@auth_google_routes.get("/iniciar_sesion/callback")
def callback():
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
        return (
            "El email del usuario no esta disponible o no ha sido verificado por Google.",
            400,
        )

    logger_info(userinfo_response.json())

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

    # Send user back to homepage
    return redirect(
        url_for("auth_routes.auth_google_routes.bienvenido")
    )


@auth_google_routes.get("/bienvenido")
def bienvenido():
    return render_template("auth/bienvenido.html")


@auth_google_routes.get("/cerrar_sesion_google")
def logout():
    logout_user()
    return redirect(url_for("index"))

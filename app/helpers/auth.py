from flask import current_app
import requests


def authenticated(session):
    "Retorna el id de usuario almacenado en la session en caso de existir"
    return session.get("user")


def get_google_provider_cfg():
    return requests.get(
        current_app.config["GOOGLE_DISCOVERY_URL"]
    ).json()

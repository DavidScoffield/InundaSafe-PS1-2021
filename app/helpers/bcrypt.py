# from flask import current_app
from flask_bcrypt import Bcrypt

flask_bcrypt = Bcrypt()


def generate_password_hash(password: str):
    "Genera con la herramienta bcrypt una contraseña hasheada y la devuelve"
    pw_hash = flask_bcrypt.generate_password_hash(password).decode("utf-8")
    return pw_hash


def check_password(hash_pass: str, password_to_check: str):
    """
    Comprueba que la contraseña que se pasa hasheada sea la misma que la otra pasada

    Parametros:
    - hash_pass : string -> contraseña hasheada
    - password_to_check : string -> contraseña a ser comprobada
    """

    return flask_bcrypt.check_password_hash(hash_pass, password_to_check)

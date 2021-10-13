from os import path, environ
from flask import Flask, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from config import config
from app import db
from app.resources.meeting_point import meeting_point
from app.resources import user
from app.resources import auth
# from app.resources.api.issue import issue_api
from app.resources.user import user as user_blueprint
from app.helpers import is_admin as helper_is_admin

from app.helpers.pruebas import modelsTest
from app.resources.config import config_routes
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import config as helper_config
from app.helpers.import_models import *


# ----- Logger -----
# import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# ------------------

load_dotenv()  # take environment variables from .env.


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Setea bootstrap para la aplicacion
    bootstrap = Bootstrap(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Configure db
    db.init_app(app)

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(helper_is_admin=helper_is_admin.is_admin)
    app.jinja_env.globals.update(get_actual_config=helper_config.actual_config)

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    app.add_url_rule("/home_privada", "home_private", auth.login_private)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # # Rutas de Consultas
    # app.add_url_rule("/consultas", "issue_index", issue.index)
    # app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    # app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # # Rutas de Usuarios
    app.register_blueprint(user_blueprint)
    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)

    # Rutas pagina configuracion(usando Blueprints)
    app.register_blueprint(config_routes)

    # Rutas página meeting points (usando Blueprints)
    app.register_blueprint(meeting_point)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app

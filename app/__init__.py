from os import environ
from flask import Flask, render_template, Blueprint
from flask_session import Session
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from app.helpers.format_role import (
    format_role as helper_format_role,
)
from config import config
from app import db
from app.resources import auth
from app.resources.home import home as home_route
from app.resources.meeting_point import meeting_point
from app.resources.flood_zones import flood_zones
from app.resources.evacuation_route import evacuation_route
from app.resources.complaint import complaint_route
from app.resources.complaint_follow_up import (
    follow_up_route,
)
from app.resources.user import user as user_blueprint
from app.resources.config import config_routes
from app.resources.auth import auth_routes

from app.resources.api.flood_zones import flood_zones_api
from app.resources.api.complaint import complaint_api
from app.resources.api.color import color_api
from app.resources.api.evacuation_route import (
    evacuation_route_api,
)
from app.resources.api.meeting_point import (
    meeting_point_api,
)

from app.helpers import handler
from app.helpers import (
    check_permission as helper_permissions,
)
from app.helpers import has_role as helper_has_role
from app.helpers import auth as helper_auth
from app.helpers import config as helper_config
from app.helpers import user as helper_user
from app.helpers import (
    complaint_is_finished as helper_complaint_is_finished,
)
from app.helpers import (
    is_admin_or_is_my_complaint as helper_is_admin_or_is_my_complaint,
)
from app.helpers.import_models import *
from flask_cors import CORS

# ----- Logger -----
# import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# ------------------

load_dotenv()  # take environment variables from .env.


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

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
    app.jinja_env.globals.update(
        is_authenticated=helper_auth.authenticated
    )
    app.jinja_env.globals.update(
        helper_has_role=helper_has_role.has_role
    )
    app.jinja_env.globals.update(
        get_actual_config=helper_config.actual_config
    )
    app.jinja_env.globals.update(
        get_user_info=helper_user.logged_user_info
    )
    app.jinja_env.globals.update(
        format_role=helper_format_role
    )
    app.jinja_env.globals.update(
        translate_state=lambda state: "Publicado"
        if state == "publicated"
        else "Despublicado"
    )
    app.jinja_env.globals.update(
        translate_users_active=lambda active: "Activo"
        if active == 1
        else "Bloqueado"
    )
    app.jinja_env.globals.update(
        helper_has_permission=helper_permissions.check_permission
    )
    app.jinja_env.globals.update(
        complaint_is_finished=helper_complaint_is_finished.complaint_is_finished
    )
    app.jinja_env.globals.update(
        is_admin_or_is_my_complaint=helper_is_admin_or_is_my_complaint.is_admin_or_is_my_complaint
    )

    # Ruta HOME
    app.register_blueprint(home_route)

    # Rutas Autenticación
    app.register_blueprint(auth_routes)

    # # Rutas de Usuarios
    app.register_blueprint(user_blueprint)

    # Rutas pagina configuracion(usando Blueprints)
    app.register_blueprint(config_routes)

    # Rutas página meeting points (usando Blueprints)
    app.register_blueprint(meeting_point)

    # Rutas página zonas inundables (usando Blueprints)
    app.register_blueprint(flood_zones)

    # Rutas página evacuation routes (usando Blueprints)
    app.register_blueprint(evacuation_route)

    # APIS
    api = Blueprint("api", __name__, url_prefix="/api")
    # Register of apis
    api.register_blueprint(flood_zones_api)
    api.register_blueprint(complaint_api)
    api.register_blueprint(evacuation_route_api)
    api.register_blueprint(meeting_point_api)
    api.register_blueprint(color_api)

    app.register_blueprint(api)
    # Rutas página complaint (usando Blueprints)
    app.register_blueprint(complaint_route)

    # Rutas página followUp (usando Blueprints)
    app.register_blueprint(follow_up_route)

    # Handlers
    app.register_error_handler(
        400, handler.bad_request_error
    )
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(
        401, handler.unauthorized_error
    )
    app.register_error_handler(
        405, handler.not_allowed_error
    )
    app.register_error_handler(
        500, handler.internal_server_error
    )
    app.config["JSON_SORT_KEYS"] = False
    # Retornar la instancia de app configurada
    return app

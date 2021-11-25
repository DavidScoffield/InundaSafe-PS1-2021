from os import environ, urandom


class Config(object):
    """Base configuration."""

    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"
    SECRET_KEY = "secret"
    UPLOAD_EXTENSIONS = [".csv"]
    UPLOAD_FOLDER = "app/static/uploads"

    # Google api configuration
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = environ.get(
        "GOOGLE_CLIENT_SECRET", None
    )
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    SECRET_KEY = environ.get("SECRET_KEY", urandom(24))

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class ProductionConfig(Config):
    """Production configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "grupo24")
    DB_PASS = environ.get("DB_PASS", "M2MzZjBlMzZlOWRj")
    DB_NAME = environ.get("DB_NAME", "grupo24")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    REDIRECT_URI_GOOGLE = "https://admin-grupo24.proyecto2021.linti.unlp.edu.ar/auth/google/iniciar_sesion/callback"


class DevelopmentConfig(Config):
    """Development configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    DB_PORT = environ.get("DB_PORT", "3306")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    REDIRECT_URI_GOOGLE = "https://127.0.0.1:5000/auth/google/iniciar_sesion/callback"


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")


config = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig,
)

# More information
# https://flask.palletsprojects.com/en/2.0.x/config/

import unittest
from app.db import db
from app import create_app
from app.models.configuration import Configuration
from app.models.colors import Color

class BaseTestClass(unittest.TestCase):

    def setUp(self):
        """
        Crea la aplicación y datos iniciales para comenzar a hacer pruebas
        """

        self.app = create_app(environment = "test")
        with self.app.app_context():
            db.create_all()
            color = Color('#00D9F5','#00F5A0','#C6FCE5','#63FFC2','#F5FFFD')
            db.session.add(color)
            db.session.commit()
            configuration = Configuration(50, 'asc', color.id, color.id)
            db.session.add(configuration)
            db.session.commit()

    def tearDown(self):
        """
        Elimina los datos de las pruebas
        """

        with self.app.app_context():
            db.session.remove()
            db.drop_all()
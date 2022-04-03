import unittest
from app.db import db
from app import create_app

class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()
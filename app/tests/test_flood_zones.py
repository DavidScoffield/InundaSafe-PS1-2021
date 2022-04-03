from . import BaseTestClass
from app.models.flood_zones import FloodZones
from app.db import db

class TestFloodZoneMethods(BaseTestClass):

    def setUp(self):
        """
        Crea algunas zonas de inundación para hacer los tests
        """
        
        super().setUp()
        with self.app.app_context():
            db.create_all()

    def test_find_by_id(self):
        """
        Se verifica que se retorne la zona inundable correspondiente a un id dado
        """
        
        with self.app.app_context():
            pass

    def test_find_by_name(self):
        """
        Se verifica que se retorne una zona inundable con un nombre dado
        """

        with self.app.app_context():
            pass

    def test_delete_coordinates(self):
        """
        Se verifica que se eliminen todas las coordenadas de una zona inundable
        """
        
        pass

    def test_add_coordinates(self):
        """
        Se verifica que se agreguen las coordenadas recibidas a la zona inundable
        """

        pass

    def test_delete(self):
        """
        Se verifica que una zona inundable se elimina correctamente
        """

        pass
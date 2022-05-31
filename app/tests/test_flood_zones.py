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
            flood_zone = FloodZones("Ejemplo1", "publicated", "#F50F00", [[1, 1], [2, 2], [3, 3]])
            db.session.add(flood_zone)
            flood_zone = FloodZones("Ejemplo2", "despublicated", "#F50F01", [[4, 4], [5, 5], [6, 6]])
            db.session.add(flood_zone)
            flood_zone = FloodZones("Ejemplo3", "publicated", "#F50F02", [[7, 7], [8, 8], [9, 9]])
            db.session.add(flood_zone)
            db.session.commit()

    def test_find_by_id(self):
        """
        Se verifica que se retorne la zona inundable correspondiente a un id dado
        """
        
        with self.app.app_context():
            buscado = FloodZones.query.get(1)
            encontrado = FloodZones.find_by_id(2)
            self.assertNotEqual(buscado, encontrado)
            encontrado = FloodZones.find_by_id(1)
            self.assertEqual(buscado, encontrado)

    def test_find_by_name(self):
        """
        Se verifica que se retorne una zona inundable con un nombre dado
        """

        with self.app.app_context():
            self.assertIsNone(FloodZones.find_by_name("Ejemplo4"))
            self.assertEqual(FloodZones.find_by_name("Ejemplo1"), FloodZones.query.get(1))

    def test_delete_coordinates(self):
        """
        Se verifica que se eliminen todas las coordenadas de una zona inundable
        """

        with self.app.app_context():
            flood_zone = FloodZones.query.get(1)
            self.assertNotEqual(len(flood_zone.coordinates), 0)
            flood_zone.delete_coordinates()
            self.assertEqual(len(flood_zone.coordinates), 0)

    def test_add_coordinates(self):
        """
        Se verifica que se agreguen las coordenadas recibidas a la zona inundable
        """

        with self.app.app_context():
            flood_zone = FloodZones.query.get(1)
            self.assertEqual(len(flood_zone.coordinates), 3)
            nuevas_coordenadas = [5, 5]
            self.assertNotEqual(flood_zone.coordinates[-1].as_array(), nuevas_coordenadas)
            flood_zone.add_coordinates([nuevas_coordenadas])
            self.assertEqual(len(flood_zone.coordinates), 4)
            self.assertEqual(flood_zone.coordinates[-1].as_array(), nuevas_coordenadas)

    def test_delete(self):
        """
        Se verifica que una zona inundable se elimina correctamente
        """

        with self.app.app_context():
            flood_zone = FloodZones.query.get(1)
            self.assertIsNotNone(flood_zone)
            flood_zone.delete()
            flood_zone = FloodZones.query.get(1)
            self.assertIsNone(flood_zone)
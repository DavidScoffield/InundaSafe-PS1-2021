from . import BaseTestClass
from app.models.evacuation_route import EvacuationRoute
from app.db import db

class TestEvacuationRouteMethods(BaseTestClass):

    def setUp(self):
        """
        Crea algunos recorridos de evacuación para hacer los tests
        """

        super().setUp()
        with self.app.app_context():
            db.create_all()

    def test_all(self):
        """
        Se verifica que se retornen todos los recorridos de evacuación publicados y paginados
        """

        with self.app.app_context():
            pass

    def test_exists_name(self):
        """
        Se verifica si en la base de datos existe otro recorrido de evacuación con un nombre dado
        """

        with self.app.app_context():
            pass

    def test_search(self):
        """
        Se verifica que se retorna una lista con los recorridos de evacuación paginados y 
        teniendo en cuenta los filtros
        """
        
        with self.app.app_context():
            pass

    def test_paginate(self):
        """
        Se verifica que se retorne una lista de recorridos paginados en base a la cantidad máxima 
        de páginas configurada en el sistema
        """

        with self.app.app_context():
            pass

    def test_new(self):
        """
        Se verifica que se cree un nuevo recorrido y se almacene en la base de datos
        """

        with self.app.app_context():
            pass

    def test_update(self):
        """
        Se verifica que se actualicen los datos del recorrido de evacuación
        """
        
        with self.app.app_context():
            pass
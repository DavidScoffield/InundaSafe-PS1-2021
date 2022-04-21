from . import BaseTestClass
from app.models.evacuation_route import EvacuationRoute
from app.models.configuration import Configuration
from app.db import db

class TestEvacuationRouteMethods(BaseTestClass):

    def setUp(self):
        """
        Crea algunos recorridos de evacuación para hacer los tests
        """

        super().setUp()
        with self.app.app_context():
            evacuation_route = EvacuationRoute("Ejemplo1", "Descripcion1", [[1, 1], [2, 2], [3, 3]], "publicated")
            db.session.add(evacuation_route)
            evacuation_route = EvacuationRoute("Ejemplo2", "Descripcion2", [[4, 4], [5, 5], [6, 6]], "despublicated")
            db.session.add(evacuation_route)
            evacuation_route = EvacuationRoute("Ejemplo3", "Descripcion3", [[6, 6], [7, 7], [8, 8]], "publicated")
            db.session.add(evacuation_route)
            db.session.commit()

    def test_all(self):
        """
        Se verifica que se retornen todos los recorridos de evacuación publicados y paginados
        """

        with self.app.app_context():
            recorridos = EvacuationRoute.all().items

            self.assertEqual(len(recorridos), 2)
            self.assertEqual(recorridos[0], EvacuationRoute.query.get(1))
            self.assertEqual(recorridos[1], EvacuationRoute.query.get(3))

            config = Configuration.query.get(1)
            config.update(50, 'desc', 1, 1)
            
            recorridos = EvacuationRoute.all().items

            self.assertEqual(len(recorridos), 2)
            self.assertEqual(recorridos[0], EvacuationRoute.query.get(3))
            self.assertEqual(recorridos[1], EvacuationRoute.query.get(1))

            config.update(1, 'desc', 1, 1)

            recorridos = EvacuationRoute.all(page = 1).items

            self.assertEqual(len(recorridos), 1)
            self.assertEqual(recorridos[0], EvacuationRoute.query.get(3))

            recorridos = EvacuationRoute.all(page = 2).items

            self.assertEqual(len(recorridos), 1)
            self.assertEqual(recorridos[0], EvacuationRoute.query.get(1))

            try:
                EvacuationRoute.all(page = 3).items
            except:
                pagina_encontrada = False
            else:
                pagina_encontrada = True

            self.assertFalse(pagina_encontrada)

    def test_exists_name(self):
        """
        Se verifica si en la base de datos existe otro recorrido de evacuación con un nombre dado
        """

        with self.app.app_context():
            self.assertFalse(EvacuationRoute.exists_name("Ejemplo4"))
            self.assertTrue(EvacuationRoute.exists_name("Ejemplo1"))

    def test_search(self):
        """
        Se verifica que se retorna una lista con los recorridos de evacuación paginados y 
        teniendo en cuenta los filtros
        """
        
        with self.app.app_context():
            config = Configuration.query.get(1)
            recorridos = EvacuationRoute.query.all()

            publicados = EvacuationRoute.search(page_number = 1, name = "Ejemplo", state = "publicated").items

            self.assertEqual(len(publicados), 2)
            self.assertEqual(publicados[0], recorridos[0])
            self.assertEqual(publicados[1], recorridos[2])

            publicados = EvacuationRoute.search(page_number = 2, name = "Ejemplo", state = "publicated").items

            self.assertEqual(len(publicados), 0)

            config.update(1, 'desc', 1, 1)

            publicados = EvacuationRoute.search(page_number = 1, name = "Ejemplo", state = "publicated").items

            self.assertEqual(len(publicados), 1)
            self.assertEqual(publicados[0], recorridos[2])

            publicados = EvacuationRoute.search(page_number = 2, name = "Ejemplo", state = "publicated").items

            self.assertEqual(len(publicados), 1)
            self.assertEqual(publicados[0], recorridos[0])

            publicados = EvacuationRoute.search(page_number = 1, name = "Ejemplo1", state = "despublicated").items

            self.assertEqual(len(publicados), 0)

    def test_new(self):
        """
        Se verifica que se cree un nuevo recorrido y se almacene en la base de datos
        """

        with self.app.app_context():
            self.assertIsNone(EvacuationRoute.query.get(4))
            args = {"name" : "Ejemplo4", "description" : "Descripcion4", "coordinates" : [[9, 9], [10, 10]], "state" : "publicated"}
            EvacuationRoute.new(**args)
            agregado = EvacuationRoute.query.get(4)
            self.assertIsNotNone(agregado)
            self.assertEqual(args["name"], agregado.name)
            self.assertEqual(args["description"], agregado.description)
            self.assertEqual(args["state"], agregado.state)
            self.assertEqual(len(args["coordinates"]), len(agregado.coordinates))
            for coord_args, coord_agregado in zip(args["coordinates"], agregado.coordinates):
                self.assertEqual(coord_args, coord_agregado.as_array())

    def test_update(self):
        """
        Se verifica que se actualicen los datos del recorrido de evacuación
        """
        
        with self.app.app_context():
            recorrido = EvacuationRoute.query.get(1)
            args = {"name" : "NuevoNombre", "description" : "NuevaDescripcion", "coordinates" : [[0, 0], [1, 1]], "state" : "despublicated"}
            recorrido.update(**args)
            self.assertEqual(args["name"], recorrido.name)
            self.assertEqual(args["description"], recorrido.description)
            self.assertEqual(args["state"], recorrido.state)
            self.assertEqual(len(args["coordinates"]), len(recorrido.coordinates))
            for coord_args, coord_recorrido in zip(args["coordinates"], recorrido.coordinates):
                self.assertEqual(coord_args, coord_recorrido.as_array())
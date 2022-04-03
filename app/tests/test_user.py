from . import BaseTestClass
from app.models.user import User
from app.db import db

class TestUserMethods(BaseTestClass):

    def setUp(self):
        """
        Crea algunos usuarios para hacer los tests
        """

        super().setUp()
        with self.app.app_context():
            db.create_all()
            new_user = User("admin@gmail.com", "administrador", "Admin123", "Cosme", "Fulanito", 1, 0, 0)
            db.session.add(new_user)
            new_user = User("ron@gmail.com", "operador1", "Operador123", "Ron", "Perez", 1, 0, 0)
            db.session.add(new_user)
            db.session.commit()

    def test_verify_password(self):
        """
        Se verifica que la contraseña ingresada se corresponda con la contraseña del usuario, la cuál 
        está hasheada y almacenada en la base de datos
        """
        
        with self.app.app_context():
            user = User.query.get(1) # usuario administrador (admin@gmail.com)
            self.assertTrue(user.verify_password("Admin123"))
            self.assertFalse(user.verify_password("Admin12345"))

    def test_delete_user(self):
        """
        Se verifica que el usuario se elimine lógicamente de la base de datos
        """

        with self.app.app_context():
            User.delete_user(1)
            self.assertTrue(User.query.get(1).is_deleted == 1)

    def test_find_by_email_and_pass(self):
        """
        Se verifica si en la base de datos existe un usuario con un email y contraseña dados
        """

        with self.app.app_context():
            self.assertIsNotNone(User.find_by_email_and_pass("admin@gmail.com", "Admin123"))
            self.assertIsNone(User.find_by_email_and_pass("admin@gmail.com", "Admin14234"))
            self.assertIsNone(User.find_by_email_and_pass("otroadmin@gmail.com", "Admin1423"))

    def test_find_user_by_id(self):
        """
        Se verifica que se retorne el usuario con el id buscado
        """

        with self.app.app_context():
            buscado = User.query.get(1)
            encontrado = User.find_user_by_id(2)
            self.assertNotEqual(buscado, encontrado)
            encontrado = User.find_user_by_id(1)
            self.assertEqual(buscado, encontrado)

    def test_find_user_by_id_not_deleted(self):
        """
        Se verifica que el id retornado se corresponda con el del usuario buscado y que no esté borrado logicamente
        """
        
        with self.app.app_context():
            buscado = User.query.get(2)
            encontrado = User.find_user_by_id_not_deleted(1)
            self.assertNotEqual(buscado, encontrado)
            encontrado = User.find_user_by_id_not_deleted(2)
            self.assertEqual(buscado, encontrado)

    def test_check_existing_email_or_username(self):
        """
        Se verifica que en la base de datos no exista otro usuario con el mismo email o nombre de usuario
        """

        with self.app.app_context():
            self.assertIsNone(User.check_existing_email_or_username(email = "ejemplo@gmail.com", username = "ejemplo"))
            self.assertIsNotNone(User.check_existing_email_or_username(email = "admin@gmail.com", username = "ejemplo"))
            self.assertIsNotNone(User.check_existing_email_or_username(email = "ejemplo@gmail.com", username = "administrador"))
from django.test import TestCase
from django.db import IntegrityError
from core.models import Usuario
from seguridad.models import Rol


class UsuarioModelTest(TestCase):
    """Pruebas unitarias para el modelo Usuario."""

    def setUp(self):
        """Crea un rol para asignar a los usuarios de prueba."""
        self.rol = Rol.objects.create(nombre="Propietario")

    def test_crear_usuario_valido(self):
        """Verifica que se pueda crear un usuario con los campos obligatorios."""
        usuario = Usuario.objects.create_user(
            username="testuser",
            password="testpass123",
            rol=self.rol
        )
        self.assertEqual(usuario.username, "testuser")
        self.assertTrue(usuario.check_password("testpass123"))
        self.assertEqual(usuario.rol, self.rol)
        self.assertTrue(usuario.is_active)

    def test_username_unico(self):
        """Verifica que no se pueda duplicar el nombre de usuario."""
        Usuario.objects.create_user(
            username="testuser",
            password="testpass123",
            rol=self.rol
        )
        with self.assertRaises(IntegrityError):
            Usuario.objects.create_user(
                username="testuser",
                password="otherpass456",
                rol=self.rol
            )

    def test_str_method(self):
        """Verifica que el método __str__ devuelva el nombre de usuario."""
        usuario = Usuario.objects.create_user(
            username="testuser",
            password="testpass123",
            rol=self.rol
        )
        self.assertEqual(str(usuario), "testuser")

    def test_usuario_sin_rol(self):
        """Verifica que se pueda crear un usuario sin rol (rol=None)."""
        usuario = Usuario.objects.create_user(
            username="sinrol",
            password="testpass123"
        )
        self.assertIsNone(usuario.rol)
        self.assertTrue(usuario.is_active)
        
    def test_autenticacion_password(self):
        """Verifica que el password se almacene como hash y se pueda verificar."""
        usuario = Usuario.objects.create_user(
        username="authuser",
        password="testpass123",
        rol=self.rol
    )
        self.assertTrue(usuario.check_password("testpass123"))
        self.assertFalse(usuario.check_password("incorrecta"))

    def test_relacion_rol(self):
        """Verifica que el rol se pueda cambiar y que se refleje en la consulta inversa."""
        usuario = Usuario.objects.create_user(
        username="roluser",
        password="testpass123",
        rol=self.rol
    )
        self.assertEqual(usuario.rol.nombre, "Propietario")
        # Cambiar de rol
        nuevo_rol = Rol.objects.create(nombre="Recepcionista")
        usuario.rol = nuevo_rol
        usuario.save()
        self.assertEqual(usuario.rol.nombre, "Recepcionista")
    # Verificar que el usuario aparece en la relación inversa del rol
        self.assertIn(usuario, nuevo_rol.usuario_set.all())
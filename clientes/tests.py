from django.test import TestCase
from django.db import IntegrityError
from clientes.models import Cliente, Vehiculo
from django.db import transaction

class ClienteModelTest(TestCase):
    """Pruebas unitarias para el modelo Cliente."""

    def test_crear_cliente_valido(self):
        """Verifica que se pueda crear un cliente con los campos obligatorios."""
        cliente = Cliente.objects.create(
            nombre="Juan Pérez",
            telefono="8095551212"
        )
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.telefono, "8095551212")
        self.assertTrue(cliente.activo)  # Por defecto debe ser True
        self.assertIsNone(cliente.cedula)  # Opcional, debe ser None
        self.assertIsNone(cliente.correo)

    def test_telefono_unico(self):
        """Verifica que no se pueda duplicar el teléfono."""
        Cliente.objects.create(nombre="Cliente Uno", telefono="8095551212")
        # Intentar crear otro cliente con el mismo teléfono debe lanzar IntegrityError
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nombre="Cliente Dos", telefono="8095551212")

    

    def test_cedula_unica_opcional(self):
        """Verifica que si se proporciona cédula, no se duplique, pero que permita nulos."""
        Cliente.objects.create(nombre="Cliente Uno", telefono="8090001111", cedula="001-1234567-8")
        # Otro cliente con la misma cédula debe fallar
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Cliente.objects.create(nombre="Cliente Dos", telefono="8090002222", cedula="001-1234567-8")
        # Cliente sin cédula no debe dar problema
        Cliente.objects.create(nombre="Cliente Tres", telefono="8090003333")  # sin cédula
    def test_str_method(self):
        """Verifica que el método __str__ devuelva el formato esperado."""
        cliente = Cliente.objects.create(
            nombre="María Gómez",
            telefono="8295555678"
        )
        esperado = "María Gómez (8295555678)"
        self.assertEqual(str(cliente), esperado)

    def test_eliminacion_logica(self):
        """Verifica que la eliminación lógica funcione correctamente."""
        cliente = Cliente.objects.create(
            nombre="Pedro Martínez",
            telefono="8095559012"
        )
        # Simular eliminación lógica
        cliente.activo = False
        cliente.save()
        # Recuperar de la base de datos
        cliente_refrescado = Cliente.objects.get(pk=cliente.pk)
        self.assertFalse(cliente_refrescado.activo)

    def test_orden_por_defecto(self):
        """Verifica que el orden por defecto sea alfabético."""
        Cliente.objects.create(nombre="Zara", telefono="8090000001")
        Cliente.objects.create(nombre="Ana", telefono="8090000002")
        clientes = Cliente.objects.all()
        self.assertEqual(clientes[0].nombre, "Ana")
        self.assertEqual(clientes[1].nombre, "Zara")

# Create your tests here.
class VehiculoModelTest(TestCase):
    """Pruebas unitarias para el modelo Vehiculo."""

    def setUp(self):
        """Crea un cliente que se usará como referencia en las pruebas."""
        self.cliente = Cliente.objects.create(
            nombre="Cliente Genérico",
            telefono="8095550000"
        )

    def test_crear_vehiculo_valido(self):
        """Verifica que se pueda crear un vehículo con los campos obligatorios."""
        vehiculo = Vehiculo.objects.create(
            placa="A123456",
            marca="Toyota",
            modelo="Corolla",
            anio=2020,
            cliente=self.cliente
        )
        self.assertEqual(vehiculo.placa, "A123456")
        self.assertEqual(vehiculo.marca, "Toyota")
        self.assertEqual(vehiculo.modelo, "Corolla")
        self.assertEqual(vehiculo.anio, 2020)
        self.assertTrue(vehiculo.activo)
        self.assertIsNone(vehiculo.chasis)
        self.assertIsNone(vehiculo.color)

    def test_placa_unica(self):
        """Verifica que no se pueda duplicar la placa."""
        Vehiculo.objects.create(
            placa="A123456", marca="Toyota", modelo="Corolla",
            anio=2020, cliente=self.cliente
        )
        with self.assertRaises(IntegrityError):
            Vehiculo.objects.create(
                placa="A123456", marca="Honda", modelo="Civic",
                anio=2021, cliente=self.cliente
            )

    def test_chasis_unico_opcional(self):
        """Verifica que el chasis sea único si se proporciona, pero permita nulos."""
        Vehiculo.objects.create(
            placa="Z0001", marca="Toyota", modelo="Yaris",
            anio=2019, cliente=self.cliente, chasis="CHASIS001"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vehiculo.objects.create(
                    placa="Z0002", marca="Honda", modelo="Fit",
                    anio=2020, cliente=self.cliente, chasis="CHASIS001"
                )
        Vehiculo.objects.create(
            placa="Z0003", marca="Ford", modelo="Focus",
            anio=2021, cliente=self.cliente
        )

    def test_relacion_cliente(self):
        """Verifica la relación con el cliente."""
        vehiculo = Vehiculo.objects.create(
            placa="B9999", marca="Nissan", modelo="Sentra",
            anio=2022, cliente=self.cliente
        )
        self.assertEqual(vehiculo.cliente, self.cliente)
        self.assertIn(vehiculo, self.cliente.vehiculos.all())

    def test_str_method(self):
        """Verifica el método __str__."""
        vehiculo = Vehiculo.objects.create(
            placa="C5555", marca="Kia", modelo="Rio",
            anio=2023, cliente=self.cliente
        )
        esperado = "C5555 - Kia Rio (2023)"
        self.assertEqual(str(vehiculo), esperado)

    def test_eliminacion_logica(self):
        """Verifica que la eliminación lógica funcione."""
        vehiculo = Vehiculo.objects.create(
            placa="D4444", marca="Hyundai", modelo="Tucson",
            anio=2021, cliente=self.cliente
        )
        vehiculo.activo = False
        vehiculo.save()
        vehiculo_refrescado = Vehiculo.objects.get(pk=vehiculo.pk)
        self.assertFalse(vehiculo_refrescado.activo)

    def test_orden_por_defecto(self):
        """Verifica el orden por marca y modelo."""
        Vehiculo.objects.create(
            placa="ORD1", marca="Zeta", modelo="A", anio=2020, cliente=self.cliente
        )
        Vehiculo.objects.create(
            placa="ORD2", marca="Alfa", modelo="B", anio=2021, cliente=self.cliente
        )
        vehiculos = Vehiculo.objects.all()
        self.assertEqual(vehiculos[0].marca, "Alfa")
        self.assertEqual(vehiculos[1].marca, "Zeta")
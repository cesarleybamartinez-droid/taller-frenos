from django.test import TestCase
from django.db import IntegrityError
from clientes.models import Cliente, Vehiculo, Marca, ModeloVehiculo
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
    """Pruebas unitarias para el modelo Vehiculo (con FK a Marca y ModeloVehiculo)."""

    def setUp(self):
        """Crea un cliente y las marcas/modelos necesarios para las pruebas."""
        self.cliente = Cliente.objects.create(
            nombre="Cliente Genérico",
            telefono="8095550000"
        )
        # Marcas
        self.toyota = Marca.objects.create(nombre="Toyota")
        self.honda = Marca.objects.create(nombre="Honda")
        self.hyundai = Marca.objects.create(nombre="Hyundai")
        self.kia = Marca.objects.create(nombre="Kia")
        self.nissan = Marca.objects.create(nombre="Nissan")
        self.zeta = Marca.objects.create(nombre="Zeta")
        self.alfa = Marca.objects.create(nombre="Alfa")
        # Modelos
        self.corolla = ModeloVehiculo.objects.create(nombre="Corolla", marca=self.toyota)
        self.civic = ModeloVehiculo.objects.create(nombre="Civic", marca=self.honda)
        self.tucson = ModeloVehiculo.objects.create(nombre="Tucson", marca=self.hyundai)
        self.rio = ModeloVehiculo.objects.create(nombre="Rio", marca=self.kia)
        self.sentra = ModeloVehiculo.objects.create(nombre="Sentra", marca=self.nissan)
        self.yaris = ModeloVehiculo.objects.create(nombre="Yaris", marca=self.toyota)
        self.modelo_a = ModeloVehiculo.objects.create(nombre="A", marca=self.zeta)
        self.modelo_b = ModeloVehiculo.objects.create(nombre="B", marca=self.alfa)

    def test_crear_vehiculo_valido(self):
        """Verifica que se pueda crear un vehículo con los campos obligatorios."""
        vehiculo = Vehiculo.objects.create(
            placa="A123456",
            marca=self.toyota,
            modelo=self.corolla,
            anio=2020,
            cliente=self.cliente
        )
        self.assertEqual(vehiculo.placa, "A123456")
        self.assertEqual(vehiculo.marca, self.toyota)
        self.assertEqual(vehiculo.modelo, self.corolla)
        self.assertEqual(vehiculo.anio, 2020)
        self.assertTrue(vehiculo.activo)
        self.assertIsNone(vehiculo.chasis)
        self.assertIsNone(vehiculo.color)

    def test_placa_unica(self):
        """Verifica que no se pueda duplicar la placa."""
        Vehiculo.objects.create(
            placa="A123456", marca=self.toyota, modelo=self.corolla,
            anio=2020, cliente=self.cliente
        )
        with self.assertRaises(IntegrityError):
            Vehiculo.objects.create(
                placa="A123456", marca=self.honda, modelo=self.civic,
                anio=2021, cliente=self.cliente
            )

    def test_chasis_unico_opcional(self):
        """Verifica que el chasis sea único si se proporciona, pero permita nulos."""
        Vehiculo.objects.create(
            placa="Z0001", marca=self.toyota, modelo=self.yaris,
            anio=2019, cliente=self.cliente, chasis="CHASIS001"
        )
        # Intentar otro con el mismo chasis debe fallar
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vehiculo.objects.create(
                    placa="Z0002", marca=self.honda, modelo=self.civic,
                    anio=2020, cliente=self.cliente, chasis="CHASIS001"
                )
        # Vehículo sin chasis debe ser permitido
        Vehiculo.objects.create(
            placa="Z0003", marca=self.nissan, modelo=self.sentra,
            anio=2021, cliente=self.cliente
        )   # chasis=None

    def test_relacion_cliente(self):
        """Verifica la relación con el cliente."""
        vehiculo = Vehiculo.objects.create(
            placa="B9999", marca=self.nissan, modelo=self.sentra,
            anio=2022, cliente=self.cliente
        )
        self.assertEqual(vehiculo.cliente, self.cliente)
        self.assertIn(vehiculo, self.cliente.vehiculos.all())

    def test_str_method(self):
        """Verifica el método __str__."""
        vehiculo = Vehiculo.objects.create(
            placa="C5555", marca=self.kia, modelo=self.rio,
            anio=2023, cliente=self.cliente
        )
        esperado = f"C5555 - {self.kia.nombre} {self.rio.nombre} (2023)"
        self.assertEqual(str(vehiculo), esperado)

    def test_eliminacion_logica(self):
        """Verifica que la eliminación lógica funcione."""
        vehiculo = Vehiculo.objects.create(
            placa="D4444", marca=self.hyundai, modelo=self.tucson,
            anio=2021, cliente=self.cliente
        )
        vehiculo.activo = False
        vehiculo.save()
        vehiculo_refrescado = Vehiculo.objects.get(pk=vehiculo.pk)
        self.assertFalse(vehiculo_refrescado.activo)

    def test_orden_por_defecto(self):
        """Verifica el orden por marca y modelo."""
        Vehiculo.objects.create(
            placa="ORD1", marca=self.zeta, modelo=self.modelo_a,
            anio=2020, cliente=self.cliente
        )
        Vehiculo.objects.create(
            placa="ORD2", marca=self.alfa, modelo=self.modelo_b,
            anio=2021, cliente=self.cliente
        )
        vehiculos = Vehiculo.objects.all()
        self.assertEqual(vehiculos[0].marca, self.alfa)
        self.assertEqual(vehiculos[1].marca, self.zeta)
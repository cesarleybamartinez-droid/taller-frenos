from django.test import TestCase
from django.db import IntegrityError, transaction
from inventario.models import CategoriaRepuesto, Repuesto, MovimientoInventario
from core.models import Usuario
from seguridad.models import Rol

class RepuestoModelTest(TestCase):
    """Pruebas unitarias para el modelo Repuesto."""

    def setUp(self):
        """Crea una categoría base para los repuestos."""
        self.categoria = CategoriaRepuesto.objects.create(
            nombre="Pastillas"
        )

    def test_crear_repuesto_valido(self):
        """Verifica que se pueda crear un repuesto con los campos obligatorios."""
        repuesto = Repuesto.objects.create(
            codigo="P-001",
            descripcion="Pastillas delanteras",
            categoria=self.categoria,
            costo_unitario=450.00,
            precio_venta=800.00
        )
        self.assertEqual(repuesto.codigo, "P-001")
        self.assertEqual(repuesto.descripcion, "Pastillas delanteras")
        self.assertIsNone(repuesto.marca)
        self.assertEqual(repuesto.stock_actual, 0)
        self.assertEqual(repuesto.stock_minimo, 5)
        self.assertTrue(repuesto.stock_bajo)   # 0 <= 5 → True

    def test_codigo_unico(self):
        """Verifica que no se pueda duplicar el código."""
        Repuesto.objects.create(
            codigo="P-001",
            descripcion="Pastillas delanteras",
            categoria=self.categoria,
            costo_unitario=450.00,
            precio_venta=800.00
        )
        with self.assertRaises(IntegrityError):
            Repuesto.objects.create(
                codigo="P-001",
                descripcion="Pastillas traseras",
                categoria=self.categoria,
                costo_unitario=500.00,
                precio_venta=900.00
            )

    def test_stock_bajo(self):
        """Verifica la propiedad stock_bajo."""
        repuesto = Repuesto.objects.create(
            codigo="P-002",
            descripcion="Pastillas traseras",
            categoria=self.categoria,
            costo_unitario=500.00,
            precio_venta=900.00,
            stock_actual=3,
            stock_minimo=5
        )
        self.assertTrue(repuesto.stock_bajo)   # 3 <= 5

        repuesto.stock_actual = 6
        repuesto.save()
        self.assertFalse(repuesto.stock_bajo)  # 6 > 5

    def test_str_method(self):
        """Verifica el método __str__."""
        repuesto = Repuesto.objects.create(
            codigo="D-001",
            descripcion="Disco de freno delantero",
            categoria=self.categoria,
            costo_unitario=1200.00,
            precio_venta=2000.00
        )
        esperado = "D-001 - Disco de freno delantero"
        self.assertEqual(str(repuesto), esperado)

    def test_default_stock_minimo(self):
        """Verifica que el stock mínimo por defecto sea 5."""
        repuesto = Repuesto.objects.create(
            codigo="T-001",
            descripcion="Tambor trasero",
            categoria=self.categoria,
            costo_unitario=1500.00,
            precio_venta=2500.00
        )
        self.assertEqual(repuesto.stock_minimo, 5)

    def test_categoria_proteccion(self):
        """Verifica que no se pueda eliminar una categoría si tiene repuestos (PROTECT)."""
        from django.db.models.deletion import ProtectedError
        Repuesto.objects.create(
            codigo="Z-999",
            descripcion="Test proteccion",
            categoria=self.categoria,
            costo_unitario=10.00,
            precio_venta=20.00
        )
        with self.assertRaises(ProtectedError):
            self.categoria.delete()
            
class MovimientoInventarioModelTest(TestCase):
    """Pruebas unitarias para el modelo MovimientoInventario."""

    def setUp(self):
        """Crea los objetos necesarios: categoría, repuesto y usuario."""
        self.categoria = CategoriaRepuesto.objects.create(nombre="Pastillas")
        self.repuesto = Repuesto.objects.create(
            codigo="MOV-001",
            descripcion="Repuesto para movimientos",
            categoria=self.categoria,
            costo_unitario=100.00,
            precio_venta=200.00,
            stock_actual=10,
            stock_minimo=2
        )
        self.rol = Rol.objects.create(nombre="Propietario")
        self.usuario = Usuario.objects.create_user(
            username="testmov",
            password="testpass123",
            rol=self.rol
        )

    def test_crear_movimiento_entrada(self):
        """Verifica que se pueda crear un movimiento de entrada."""
        mov = MovimientoInventario.objects.create(
            repuesto=self.repuesto,
            tipo='Entrada',
            cantidad=5,
            usuario=self.usuario,
            motivo="Compra a proveedor"
        )
        self.assertEqual(mov.repuesto, self.repuesto)
        self.assertEqual(mov.tipo, 'Entrada')
        self.assertEqual(mov.cantidad, 5)
        self.assertEqual(mov.usuario, self.usuario)

    def test_crear_movimiento_salida(self):
        """Verifica que se pueda crear un movimiento de salida."""
        mov = MovimientoInventario.objects.create(
            repuesto=self.repuesto,
            tipo='Salida',
            cantidad=3,
            usuario=self.usuario,
            motivo="Usado en orden #1"
        )
        self.assertEqual(mov.tipo, 'Salida')
        self.assertEqual(mov.cantidad, 3)

    def test_crear_movimiento_ajuste(self):
        """Verifica que se pueda crear un ajuste manual."""
        mov = MovimientoInventario.objects.create(
            repuesto=self.repuesto,
            tipo='Ajuste',
            cantidad=10,
            usuario=self.usuario,
            motivo="Inventario físico"
        )
        self.assertEqual(mov.tipo, 'Ajuste')
        self.assertEqual(mov.cantidad, 10)

    def test_str_method(self):
        """Verifica el método __str__."""
        mov = MovimientoInventario.objects.create(
            repuesto=self.repuesto,
            tipo='Entrada',
            cantidad=5,
            usuario=self.usuario,
            motivo="Compra a proveedor"
        )
        esperado = f"Entrada - MOV-001 (5)"
        self.assertEqual(str(mov), esperado)

    def test_movimiento_requiere_usuario(self):
        """Verifica que el campo usuario sea obligatorio."""
        with self.assertRaises(IntegrityError):
            MovimientoInventario.objects.create(
                repuesto=self.repuesto,
                tipo='Entrada',
                cantidad=5,
                usuario=None  # Debería fallar
            )

    def test_movimiento_requiere_repuesto(self):
        """Verifica que el campo repuesto sea obligatorio."""
        with self.assertRaises(IntegrityError):
            MovimientoInventario.objects.create(
                repuesto=None,  # Debería fallar
                tipo='Entrada',
                cantidad=5,
                usuario=self.usuario
            )
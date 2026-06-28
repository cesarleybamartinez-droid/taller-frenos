from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from decimal import Decimal
from ordenes.models import OrdenTrabajo, Servicio, DetalleServicio, DetalleRepuesto, Pago
from clientes.models import Cliente, Vehiculo, Marca, ModeloVehiculo
from inventario.models import CategoriaRepuesto, Repuesto


class OrdenTrabajoModelTest(TestCase):
    """Pruebas unitarias para el modelo OrdenTrabajo y sus relaciones."""

    def setUp(self):
        """Crea los objetos necesarios para las pruebas."""
        # Cliente y vehículo
        self.cliente = Cliente.objects.create(
            nombre="Cliente Prueba",
            telefono="8095550000"
        )
        self.marca = Marca.objects.create(nombre="Toyota")
        self.modelo = ModeloVehiculo.objects.create(nombre="Corolla", marca=self.marca)
        self.vehiculo = Vehiculo.objects.create(
            placa="ORDTEST1",
            marca=self.marca,
            modelo=self.modelo,
            anio=2020,
            cliente=self.cliente
        )
        # Servicio
        self.servicio = Servicio.objects.create(
            nombre="Diagnóstico de frenos",
            precio_estandar=500.00
        )
        # Repuesto
        self.categoria = CategoriaRepuesto.objects.create(nombre="Pastillas")
        self.repuesto = Repuesto.objects.create(
            codigo="ORD-REP-001",
            descripcion="Pastillas delanteras",
            categoria=self.categoria,
            costo_unitario=450.00,
            precio_venta=800.00,
            stock_actual=10,
            stock_minimo=2
        )

    def test_crear_orden_valida(self):
        """Verifica que se pueda crear una orden de trabajo con estado Pendiente."""
        orden = OrdenTrabajo.objects.create(
            vehiculo=self.vehiculo,
            diagnostico="Chirrido al frenar",
            estado='Pendiente'
        )
        self.assertEqual(orden.vehiculo, self.vehiculo)
        self.assertEqual(orden.estado, 'Pendiente')
        self.assertEqual(orden.total, Decimal('0.00'))
        self.assertEqual(orden.saldo_pendiente, Decimal('0.00'))

    def test_propiedades_calculadas(self):
        """Verifica las propiedades total_pagado y saldo_pendiente tras agregar un pago."""
        orden = OrdenTrabajo.objects.create(
            vehiculo=self.vehiculo,
            estado='Finalizada'
        )
        # Agregar un servicio (usamos Decimal desde el principio)
        DetalleServicio.objects.create(
            orden=orden,
            servicio=self.servicio,
            cantidad=1,
            precio_unitario=Decimal('500.00'),
            subtotal=Decimal('500.00')
        )
        orden.subtotal_servicios = Decimal('500.00')
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()

        self.assertEqual(orden.total_pagado, 0)
        self.assertEqual(orden.saldo_pendiente, orden.total)

        # Registrar un pago
        Pago.objects.create(orden=orden, monto=orden.total, metodo='Efectivo')
        self.assertEqual(orden.total_pagado, orden.total)
        self.assertEqual(orden.saldo_pendiente, 0)

    def test_estados_permitidos(self):
        """Verifica que el campo estado solo acepte los valores definidos en el modelo."""
        orden = OrdenTrabajo.objects.create(
            vehiculo=self.vehiculo,
            estado='Pendiente'
        )
        # Asignar un estado válido
        orden.estado = 'En Progreso'
        orden.full_clean()   # No lanza excepción
        orden.save()
        self.assertEqual(orden.estado, 'En Progreso')

        # Intentar asignar un estado inválido debería lanzar ValidationError
        orden.estado = 'EstadoInventado'
        with self.assertRaises(ValidationError):
            orden.full_clean()

    def test_str_method(self):
        """Verifica que el método __str__ devuelva el formato esperado."""
        orden = OrdenTrabajo.objects.create(
            vehiculo=self.vehiculo,
            estado='Pendiente'
        )
        esperado = f"Orden #{orden.id} - ORDTEST1 (Pendiente)"
        self.assertEqual(str(orden), esperado)

    def test_crear_detalle_servicio(self):
        """Verifica que se pueda crear un detalle de servicio correctamente."""
        orden = OrdenTrabajo.objects.create(
            vehiculo=self.vehiculo,
            estado='Pendiente'
        )
        detalle = DetalleServicio.objects.create(
            orden=orden,
            servicio=self.servicio,
            cantidad=2,
            precio_unitario=500.00,
            subtotal=1000.00
        )
        self.assertEqual(detalle.cantidad, 2)
        self.assertEqual(detalle.subtotal, 1000.00)

    def test_crear_detalle_repuesto(self):
        """Verifica que se pueda crear un detalle de repuesto con los campos históricos."""
        orden = OrdenTrabajo.objects.create(
            vehiculo=self.vehiculo,
            estado='Pendiente'
        )
        detalle = DetalleRepuesto.objects.create(
            orden=orden,
            repuesto=self.repuesto,
            cantidad=1,
            precio_unitario=800.00,
            costo_unitario=450.00,
            subtotal=800.00
        )
        self.assertEqual(detalle.cantidad, 1)
        self.assertEqual(detalle.precio_unitario, 800.00)
        self.assertEqual(detalle.costo_unitario, 450.00)
        self.assertEqual(detalle.subtotal, 800.00)

    def test_crear_pago(self):
        """Verifica que se pueda registrar un pago asociado a una orden."""
        orden = OrdenTrabajo.objects.create(
            vehiculo=self.vehiculo,
            estado='Finalizada'
        )
        pago = Pago.objects.create(
            orden=orden,
            monto=500.00,
            metodo='Efectivo'
        )
        self.assertEqual(pago.monto, 500.00)
        self.assertEqual(pago.metodo, 'Efectivo')
        self.assertEqual(pago.orden, orden)
from django.core.management.base import BaseCommand
from clientes.models import Cliente, Vehiculo
from inventario.models import CategoriaRepuesto, Repuesto
from ordenes.models import Servicio, OrdenTrabajo, DetalleServicio, DetalleRepuesto, Pago
from seguridad.models import Rol
from core.models import Usuario
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga datos de prueba (clientes, vehículos, repuestos, órdenes)'

    def handle(self, *args, **options):
        # -------------------- CLIENTES --------------------
        clientes_data = [
            {'nombre': 'Juan Pérez', 'telefono': '809-555-1234', 'cedula': '001-1234567-8', 'correo': 'juan.perez@email.com', 'direccion': 'Calle Duarte #45, Santo Domingo'},
            {'nombre': 'María Gómez', 'telefono': '829-555-5678', 'cedula': '002-9876543-2', 'correo': 'maria.gomez@email.com', 'direccion': 'Av. Independencia #120, Santiago'},
            {'nombre': 'Pedro Martínez', 'telefono': '809-555-9012', 'cedula': '003-4567890-1', 'correo': 'pedro.martinez@email.com', 'direccion': 'Calle Mella #78, La Romana'},
            {'nombre': 'Ana Rodríguez', 'telefono': '849-555-3456', 'cedula': '004-2345678-9', 'correo': 'ana.rodriguez@email.com', 'direccion': 'Calle Sánchez #200, San Cristóbal'},
            {'nombre': 'Luis Fernández', 'telefono': '809-555-7890', 'cedula': '005-8765432-5', 'correo': 'luis.fernandez@email.com', 'direccion': 'Av. 27 de Febrero #300, Santo Domingo'},
            {'nombre': 'Carmen Díaz', 'telefono': '829-555-4321', 'cedula': '006-3456789-0', 'correo': 'carmen.diaz@email.com', 'direccion': 'Calle Colón #50, Puerto Plata'},
            {'nombre': 'José Ramírez', 'telefono': '849-555-8765', 'cedula': '007-6543210-9', 'correo': 'jose.ramirez@email.com', 'direccion': 'Calle Beller #15, San Pedro de Macorís'},
            {'nombre': 'Rosa Vargas', 'telefono': '809-555-2109', 'cedula': '008-7890123-4', 'correo': 'rosa.vargas@email.com', 'direccion': 'Av. Bolívar #80, La Vega'},
            {'nombre': 'Carlos Jiménez', 'telefono': '829-555-0987', 'cedula': '009-0123456-7', 'correo': 'carlos.jimenez@email.com', 'direccion': 'Calle del Sol #90, Santiago'},
            {'nombre': 'Laura Torres', 'telefono': '849-555-5432', 'cedula': '010-5678901-2', 'correo': 'laura.torres@email.com', 'direccion': 'Av. Winston Churchill #110, Santo Domingo'},
        ]
        clientes = []
        for data in clientes_data:
            cliente, _ = Cliente.objects.get_or_create(telefono=data['telefono'], defaults=data)
            clientes.append(cliente)
            self.stdout.write(f'Cliente {cliente.nombre} creado')

        # -------------------- VEHÍCULOS --------------------
        vehiculos_data = [
            {'placa': 'A123456', 'marca': 'Toyota', 'modelo': 'Corolla', 'anio': 2020, 'color': 'Blanco', 'chasis': 'CHA001', 'tipo_frenos': 'Disco delantero y trasero', 'cliente': clientes[0]},
            {'placa': 'B789012', 'marca': 'Honda', 'modelo': 'Civic', 'anio': 2019, 'color': 'Negro', 'chasis': 'CHA002', 'tipo_frenos': 'Disco delantero / Tambor trasero', 'cliente': clientes[1]},
            {'placa': 'C345678', 'marca': 'Nissan', 'modelo': 'Sentra', 'anio': 2021, 'color': 'Gris', 'chasis': 'CHA003', 'tipo_frenos': 'Disco delantero y trasero', 'cliente': clientes[2]},
            {'placa': 'D901234', 'marca': 'Hyundai', 'modelo': 'Elantra', 'anio': 2018, 'color': 'Azul', 'chasis': 'CHA004', 'tipo_frenos': 'Disco delantero / Tambor trasero', 'cliente': clientes[3]},
            {'placa': 'E567890', 'marca': 'Kia', 'modelo': 'Rio', 'anio': 2022, 'color': 'Rojo', 'chasis': 'CHA005', 'tipo_frenos': 'Disco delantero y trasero', 'cliente': clientes[4]},
            {'placa': 'F432109', 'marca': 'Toyota', 'modelo': 'Yaris', 'anio': 2020, 'color': 'Verde', 'chasis': 'CHA006', 'tipo_frenos': 'Disco delantero / Tambor trasero', 'cliente': clientes[5]},
            {'placa': 'G876543', 'marca': 'Honda', 'modelo': 'CR-V', 'anio': 2023, 'color': 'Plata', 'chasis': 'CHA007', 'tipo_frenos': 'Disco delantero y trasero', 'cliente': clientes[6]},
            {'placa': 'H210987', 'marca': 'Mitsubishi', 'modelo': 'Lancer', 'anio': 2017, 'color': 'Blanco', 'chasis': 'CHA008', 'tipo_frenos': 'Disco delantero / Tambor trasero', 'cliente': clientes[7]},
            {'placa': 'I098765', 'marca': 'Ford', 'modelo': 'Focus', 'anio': 2019, 'color': 'Negro', 'chasis': 'CHA009', 'tipo_frenos': 'Disco delantero y trasero', 'cliente': clientes[8]},
            {'placa': 'J543210', 'marca': 'Chevrolet', 'modelo': 'Cruze', 'anio': 2021, 'color': 'Gris', 'chasis': 'CHA010', 'tipo_frenos': 'Disco delantero / Tambor trasero', 'cliente': clientes[9]},
        ]
        vehiculos = []
        for data in vehiculos_data:
            vehiculo, _ = Vehiculo.objects.get_or_create(placa=data['placa'], defaults=data)
            vehiculos.append(vehiculo)
            self.stdout.write(f'Vehículo {vehiculo.placa} creado')

        # -------------------- REPUESTOS (usar categorías ya existentes) --------------------
        cat_pastillas = CategoriaRepuesto.objects.get(nombre='Pastillas')
        cat_discos = CategoriaRepuesto.objects.get(nombre='Discos')
        repuestos_data = [
            {'codigo': 'P-001', 'descripcion': 'Pastillas delanteras', 'marca': 'Wagner', 'categoria': cat_pastillas, 'costo_unitario': 450.00, 'precio_venta': 800.00, 'stock_actual': 8, 'stock_minimo': 5},
            {'codigo': 'P-002', 'descripcion': 'Pastillas traseras', 'marca': 'Bosch', 'categoria': cat_pastillas, 'costo_unitario': 500.00, 'precio_venta': 900.00, 'stock_actual': 3, 'stock_minimo': 5},
            {'codigo': 'D-001', 'descripcion': 'Disco de freno delantero', 'marca': 'Raybestos', 'categoria': cat_discos, 'costo_unitario': 1200.00, 'precio_venta': 2000.00, 'stock_actual': 10, 'stock_minimo': 3},
        ]
        repuestos = []
        for data in repuestos_data:
            repuesto, _ = Repuesto.objects.get_or_create(codigo=data['codigo'], defaults=data)
            repuestos.append(repuesto)
            self.stdout.write(f'Repuesto {repuesto.codigo} creado')

        # -------------------- ÓRDENES DE EJEMPLO --------------------
        # Orden #1 (Pendiente)
        o1 = OrdenTrabajo.objects.create(
            vehiculo=vehiculos[0], diagnostico='Chirrido al frenar', observaciones='Cambio de pastillas delanteras',
            estado='Pendiente', fecha_estimada_entrega='2026-06-28'
        )
        DetalleServicio.objects.create(orden=o1, servicio=Servicio.objects.get(nombre='Cambio de pastillas delanteras'), cantidad=1, precio_unitario=800.00, subtotal=800.00)
        DetalleRepuesto.objects.create(orden=o1, repuesto=repuestos[0], cantidad=1, precio_unitario=800.00, costo_unitario=450.00, subtotal=800.00)
        self._actualizar_totales(o1)

        # Orden #2 (Diagnóstico)
        o2 = OrdenTrabajo.objects.create(
            vehiculo=vehiculos[1], diagnostico='Vibración al frenar', estado='Diagnóstico'
        )
        DetalleServicio.objects.create(orden=o2, servicio=Servicio.objects.get(nombre='Diagnóstico de frenos'), cantidad=1, precio_unitario=500.00, subtotal=500.00)
        self._actualizar_totales(o2)

        # Orden #3 (En Progreso)
        o3 = OrdenTrabajo.objects.create(
            vehiculo=vehiculos[2], diagnostico='Pedal esponjoso', estado='En Progreso'
        )
        DetalleServicio.objects.create(orden=o3, servicio=Servicio.objects.get(nombre='Purga de líquido de frenos'), cantidad=1, precio_unitario=900.00, subtotal=900.00)
        self._actualizar_totales(o3)

        # Orden #4 (Finalizada con pago parcial)
        o4 = OrdenTrabajo.objects.create(
            vehiculo=vehiculos[3], diagnostico='Discos delanteros deformados', estado='Finalizada'
        )
        DetalleServicio.objects.create(orden=o4, servicio=Servicio.objects.get(nombre='Cambio de discos delanteros'), cantidad=1, precio_unitario=1200.00, subtotal=1200.00)
        DetalleRepuesto.objects.create(orden=o4, repuesto=repuestos[2], cantidad=2, precio_unitario=2000.00, costo_unitario=1200.00, subtotal=4000.00)
        self._actualizar_totales(o4)
        Pago.objects.create(orden=o4, monto=3000.00, metodo='Efectivo')

        # Orden #5 (Entregada, pagada)
        o5 = OrdenTrabajo.objects.create(
            vehiculo=vehiculos[4], diagnostico='Luz ABS encendida', estado='Entregada'
        )
        DetalleServicio.objects.create(orden=o5, servicio=Servicio.objects.get(nombre='Cambio de sensores ABS'), cantidad=1, precio_unitario=400.00, subtotal=400.00)
        self._actualizar_totales(o5)
        Pago.objects.create(orden=o5, monto=o5.total, metodo='Tarjeta')

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados exitosamente.'))

    def _actualizar_totales(self, orden):
        orden.subtotal_servicios = orden.detalleservicio_set.aggregate(t=__import__('django').db.models.Sum('subtotal'))['t'] or 0
        orden.subtotal_repuestos = orden.detallerepuesto_set.aggregate(t=__import__('django').db.models.Sum('subtotal'))['t'] or 0
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()
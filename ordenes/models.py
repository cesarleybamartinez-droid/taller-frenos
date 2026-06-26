from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Vehiculo
from inventario.models import Repuesto
from core.models import Usuario


class Servicio(models.Model):
    """Catálogo de servicios de mano de obra."""
    nombre = models.CharField(max_length=100, verbose_name="Nombre del servicio")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    precio_estandar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio estándar (RD$)")

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class OrdenTrabajo(models.Model):
    """Orden de trabajo del taller."""
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Diagnóstico', 'Diagnóstico'),
        ('Esperando Aprobación', 'Esperando Aprobación'),
        ('En Progreso', 'En Progreso'),
        ('Suspendida', 'Suspendida'),
        ('Finalizada', 'Finalizada'),
        ('Entregada', 'Entregada'),
        ('Cancelada', 'Cancelada'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, verbose_name="Vehículo")
    fecha_ingreso = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de ingreso")
    fecha_estimada_entrega = models.DateField(blank=True, null=True, verbose_name="Fecha estimada de entrega")
    fecha_entrega_real = models.DateTimeField(blank=True, null=True, verbose_name="Fecha real de entrega")
    diagnostico = models.TextField(blank=True, null=True, verbose_name="Diagnóstico")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    estado = models.CharField(max_length=25, choices=ESTADOS, default='Pendiente', verbose_name="Estado")
    subtotal_repuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Subtotal repuestos")
    subtotal_servicios = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Subtotal servicios")
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Descuento")
    itbis = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ITBIS (18%)")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total")

    class Meta:
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Órdenes de trabajo"
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo.placa} ({self.estado})"

    @property
    def cliente(self):
        return self.vehiculo.cliente

    @property
    def total_pagado(self):
        return self.pago_set.aggregate(total=models.Sum('monto'))['total'] or 0

    @property
    def saldo_pendiente(self):
        return self.total - self.total_pagado


class DetalleServicio(models.Model):
    """Servicios realizados en una orden."""
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, verbose_name="Orden")
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name="Servicio")
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Detalle de servicio"
        verbose_name_plural = "Detalles de servicios"

    def __str__(self):
        return f"{self.servicio.nombre} x{self.cantidad} - Orden #{self.orden_id}"


class DetalleRepuesto(models.Model):
    """Repuestos utilizados en una orden."""
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, verbose_name="Orden")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT, verbose_name="Repuesto")
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de venta")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario (histórico)")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Detalle de repuesto"
        verbose_name_plural = "Detalles de repuestos"

    def __str__(self):
        return f"{self.repuesto.descripcion} x{self.cantidad} - Orden #{self.orden_id}"


class Pago(models.Model):
    """Pagos registrados para una orden."""
    METODOS = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta'),
    ]
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, verbose_name="Orden")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    metodo = models.CharField(max_length=15, choices=METODOS, verbose_name="Método de pago")

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Pago RD${self.monto} - Orden #{self.orden_id}"
# Create your models here.

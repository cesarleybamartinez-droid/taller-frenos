from django.db import models
from inventario.models import Repuesto

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre comercial")
    contacto = models.CharField(max_length=100, blank=True, null=True, verbose_name="Persona de contacto")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    correo = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Correo electrónico")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name="Proveedor")
    fecha = models.DateField(verbose_name="Fecha")
    num_factura = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de factura")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total")

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha']

    def __str__(self):
        return f"Compra {self.id} - {self.proveedor.nombre} ({self.fecha})"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT, verbose_name="Repuesto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Detalle de compra"
        verbose_name_plural = "Detalles de compra"

    def __str__(self):
        return f"{self.repuesto.descripcion} x{self.cantidad} (Compra #{self.compra_id})"


class Gasto(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    descripcion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción")
    categoria = models.CharField(max_length=80, blank=True, null=True, verbose_name="Categoría")
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compra asociada")

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Gasto {self.descripcion or 'sin descripción'} - RD$ {self.monto}"
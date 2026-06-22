from django.db import models
from core.models import Usuario


class CategoriaRepuesto(models.Model):
    """Categoría de repuesto (Pastillas, Discos, Tambores, etc.)."""
    nombre = models.CharField(max_length=80, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría de repuesto"
        verbose_name_plural = "Categorías de repuestos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Repuesto(models.Model):
    """Repuesto o insumo del taller."""
    codigo = models.CharField(max_length=30, unique=True, verbose_name="Código")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    marca = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marca")
    categoria = models.ForeignKey(CategoriaRepuesto, on_delete=models.PROTECT, verbose_name="Categoría")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de venta")
    stock_actual = models.IntegerField(default=0, verbose_name="Stock actual")
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock mínimo")

    class Meta:
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"
        ordering = ['categoria', 'descripcion']

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    @property
    def stock_bajo(self):
        """Devuelve True si el stock actual es menor o igual al mínimo."""
        return self.stock_actual <= self.stock_minimo


class MovimientoInventario(models.Model):
    """Registro de cada entrada, salida o ajuste de inventario."""
    TIPO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
        ('Ajuste', 'Ajuste'),
    ]
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, verbose_name="Repuesto")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo")
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name="Usuario")

    class Meta:
        verbose_name = "Movimiento de inventario"
        verbose_name_plural = "Movimientos de inventario"
        ordering = ['-fecha']

    def __str__(self):
     return f"{self.tipo} - {self.repuesto.codigo} ({self.cantidad})"
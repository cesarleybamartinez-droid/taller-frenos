from django.db import models

class Cliente(models.Model):
    """Modelo que representa a un cliente del taller."""
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    telefono = models.CharField(max_length=20, unique=True, verbose_name="Teléfono")
    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Cédula")
    correo = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Correo electrónico")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        ordering = ['nombre']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"


class Vehiculo(models.Model):
    """Modelo que representa un vehículo asociado a un cliente."""
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    anio = models.IntegerField(verbose_name="Año")
    color = models.CharField(max_length=30, blank=True, null=True, verbose_name="Color")
    chasis = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name="Chasis")
    tipo_frenos = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tipo de frenos")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos', verbose_name="Cliente")

    class Meta:
        ordering = ['marca', 'modelo']
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.anio})"
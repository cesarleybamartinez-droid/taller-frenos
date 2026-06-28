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

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Marca")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre


class ModeloVehiculo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos', verbose_name="Marca")
    nombre = models.CharField(max_length=50, verbose_name="Modelo")

    class Meta:
        unique_together = ('marca', 'nombre')
        verbose_name = "Modelo de vehículo"
        verbose_name_plural = "Modelos de vehículos"

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


class Vehiculo(models.Model):
    """Modelo que representa un vehículo asociado a un cliente."""
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa", null=False, blank=False)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name="Marca")
    modelo = models.ForeignKey(ModeloVehiculo, on_delete=models.PROTECT, verbose_name="Modelo")
    anio = models.IntegerField(verbose_name="Año")
    color = models.CharField(max_length=30, blank=True, null=True, verbose_name="Color")
    chasis = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name="Chasis")
    tipo_frenos = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Tipo de frenos",
        choices=[
            ('Disco delantero y trasero', 'Disco delantero y trasero'),
            ('Disco delantero / Tambor trasero', 'Disco delantero / Tambor trasero'),
            ('Tambor delantero y trasero', 'Tambor delantero y trasero'),
            ('EBD', 'EBD (Electronic Brakeforce Distribution)'),
            ('BA/BAS', 'BA/BAS (Brake Assist)'),
            ('No especificado', 'No especificado'),
        ]
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos', verbose_name="Cliente")

    class Meta:
        ordering = ['marca__nombre', 'modelo__nombre']
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"{self.placa} - {self.marca.nombre} {self.modelo.nombre} ({self.anio})"
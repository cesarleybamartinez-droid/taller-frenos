from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)
    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"
# Create your models here.
class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    color = models.CharField(max_length=30, blank=True, null=True)
    chasis = models.CharField(max_length=30, unique=True, null=True, blank=True)
    tipo_frenos = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')

    class Meta:
        ordering = ['marca', 'modelo']

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.anio})"
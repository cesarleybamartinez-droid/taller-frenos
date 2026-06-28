from django.db import models

class Ingreso(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    descripcion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción")
    categoria = models.CharField(max_length=80, blank=True, null=True, verbose_name="Categoría")

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Ingreso {self.descripcion or 'sin descripción'} - RD$ {self.monto}"
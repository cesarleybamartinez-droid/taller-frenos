from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre

class Permiso(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    
    def __str__(self):
        return self.nombre

class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')

class Auditoria(models.Model):
    usuario = models.ForeignKey('core.Usuario', on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
class Auditoria(models.Model):
    usuario = models.ForeignKey('core.Usuario', on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"

    def __str__(self):
        return f"{self.fecha_hora} - {self.usuario.username} - {self.accion}"
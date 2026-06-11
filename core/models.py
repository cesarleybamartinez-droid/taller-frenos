from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Relación con Rol (la crearemos después en seguridad)
    # Por ahora solo agregamos el campo de rol como una ForeignKey nullable
    # y luego actualizaremos cuando tengamos el modelo Rol de la app seguridad
    pass



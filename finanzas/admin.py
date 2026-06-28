from django.contrib import admin
from .models import Ingreso

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'descripcion', 'monto', 'categoria')
    list_filter = ('fecha', 'categoria')
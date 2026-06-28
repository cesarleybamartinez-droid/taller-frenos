from django.contrib import admin
from .models import Rol, Permiso, RolPermiso, Auditoria

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(RolPermiso)
class RolPermisoAdmin(admin.ModelAdmin):
    list_display = ('rol', 'permiso')

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_hora')
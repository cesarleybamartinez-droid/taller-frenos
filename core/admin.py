from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario

class UsuarioAdmin(BaseUserAdmin):
    # Campos que se muestran en la lista de usuarios
    list_display = ('username', 'email', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active', 'is_staff')

    # Campos que se pueden editar al modificar un usuario
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )

    # Campos que se piden al crear un nuevo usuario
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )

admin.site.register(Usuario, UsuarioAdmin)
# Register your models here.

from django.contrib import admin
from .models import Cliente, Vehiculo, Marca, ModeloVehiculo

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'cedula', 'activo')
    search_fields = ('nombre', 'telefono')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'anio', 'cliente', 'activo')
    search_fields = ('placa',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(ModeloVehiculo)
class ModeloVehiculoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca')

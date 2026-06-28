from django.contrib import admin
from .models import Servicio, OrdenTrabajo, DetalleServicio, DetalleRepuesto, Pago

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_estandar')

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estado', 'total', 'fecha_ingreso')
    list_filter = ('estado',)

@admin.register(DetalleServicio)
class DetalleServicioAdmin(admin.ModelAdmin):
    list_display = ('orden', 'servicio', 'cantidad', 'subtotal')

@admin.register(DetalleRepuesto)
class DetalleRepuestoAdmin(admin.ModelAdmin):
    list_display = ('orden', 'repuesto', 'cantidad', 'subtotal')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('orden', 'monto', 'metodo', 'fecha')
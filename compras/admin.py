from django.contrib import admin
from .models import Proveedor, Compra, DetalleCompra, Gasto

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha', 'num_factura', 'total')
    list_filter = ('fecha', 'proveedor')

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'repuesto', 'cantidad', 'costo_unitario')

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'descripcion', 'monto', 'categoria')
    list_filter = ('fecha', 'categoria')
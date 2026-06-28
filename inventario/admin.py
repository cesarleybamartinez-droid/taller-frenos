from django.contrib import admin
from .models import CategoriaRepuesto, Repuesto, MovimientoInventario

@admin.register(CategoriaRepuesto)
class CategoriaRepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'categoria', 'stock_actual', 'precio_venta')
    search_fields = ('codigo', 'descripcion')

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('repuesto', 'tipo', 'cantidad', 'fecha', 'usuario')
    list_filter = ('tipo',)
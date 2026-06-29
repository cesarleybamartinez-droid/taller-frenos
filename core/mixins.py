from django.contrib.auth.mixins import UserPassesTestMixin

class TienePermisoMixin(UserPassesTestMixin):
    """Permite el acceso solo si el rol del usuario posee el permiso indicado."""
    permiso = None

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.rol:
            return False
        return self.request.user.rol.rolpermiso_set.filter(
            permiso__nombre=self.permiso
        ).exists()
        
class OrdenYPaginacionMixin:
    """Mixin para vistas basadas en ListView que permite ordenar por columnas
    y elegir cuántos registros por página."""
    ordering_allowed = {}   # {nombre_parametro: campo_modelo}  ej: {'nombre': 'nombre', 'telefono': 'telefono'}
    ordering_default = None  # campo por defecto

    def get_ordering(self):
        order_param = self.request.GET.get('order_by')
        direction = self.request.GET.get('dir', 'asc')
        if order_param and order_param in self.ordering_allowed:
            campo = self.ordering_allowed[order_param]
            if direction == 'desc':
                campo = '-' + campo
            return [campo]
        return [self.ordering_default] if self.ordering_default else []

    def get_paginate_by(self, queryset):
        return self.request.GET.get('per_page', 20)
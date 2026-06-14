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
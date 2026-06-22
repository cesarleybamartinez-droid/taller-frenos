from django.contrib import admin
from django.urls import path, include
from core.views import CustomLoginView, cerrar_sesion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', cerrar_sesion, name='logout'),   # <-- ahora usa GET
    path('clientes/', include('clientes.urls')),
    path('seguridad/', include('seguridad.urls')),
    path('inventario/', include('inventario.urls')),
]
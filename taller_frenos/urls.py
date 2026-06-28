from django.contrib import admin
from django.urls import path, include
from core.views import CustomLoginView, cerrar_sesion
from django.shortcuts import redirect

def redirigir_inicio(request):
    if request.user.is_authenticated:
        return redirect('clientes:cliente_list')  # Cambiar por 'dashboard' cuando exista
    else:
        return redirect('login')

urlpatterns = [
    path('', redirigir_inicio, name='inicio'),  # <-- añade esta línea
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', cerrar_sesion, name='logout'),   # <-- ahora usa GET
    path('clientes/', include('clientes.urls')),
    path('seguridad/', include('seguridad.urls')),
    path('inventario/', include('inventario.urls')),
    path('ordenes/', include('ordenes.urls')),
    
]
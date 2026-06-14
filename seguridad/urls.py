from django.urls import path
from . import views

app_name = 'seguridad'

urlpatterns = [
    # Usuarios
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/nuevo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),

    # Auditoría
    path('auditoria/', views.AuditoriaListView.as_view(), name='auditoria_list'),

 # Roles y Permisos
    path('roles/', views.RolListView.as_view(), name='rol_list'),
    path('roles/<int:pk>/permisos/', views.RolPermisoUpdateView.as_view(), name='rol_permisos'),
    
    # Eliminar Usuario
    path('usuarios/<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
]
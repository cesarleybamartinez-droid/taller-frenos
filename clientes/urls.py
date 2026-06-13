from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    # Clientes
    path('', views.ClienteListView.as_view(), name='cliente_list'),
    path('nuevo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_delete'),

    # Vehículos
    path('vehiculos/', views.VehiculoListView.as_view(), name='vehiculo_list'),
    path('vehiculos/nuevo/', views.VehiculoCreateView.as_view(), name='vehiculo_create'),
    path('vehiculos/<int:pk>/', views.VehiculoDetailView.as_view(), name='vehiculo_detail'),
    path('vehiculos/<int:pk>/editar/', views.VehiculoUpdateView.as_view(), name='vehiculo_update'),
    path('vehiculos/<int:pk>/eliminar/', views.VehiculoDeleteView.as_view(), name='vehiculo_delete'),
]
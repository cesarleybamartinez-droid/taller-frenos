from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('', views.OrdenListView.as_view(), name='orden_list'),
    path('nueva/', views.OrdenCreateView.as_view(), name='orden_create'),
    path('<int:pk>/', views.OrdenDetailView.as_view(), name='orden_detail'),
    path('<int:orden_pk>/agregar-servicio/', views.AgregarServicioView.as_view(), name='agregar_servicio'),
    path('<int:orden_pk>/agregar-repuesto/', views.AgregarRepuestoView.as_view(), name='agregar_repuesto'),
    path('<int:pk>/cambiar-estado/', views.CambiarEstadoView.as_view(), name='cambiar_estado'),
    path('<int:orden_pk>/registrar-pago/', views.RegistrarPagoView.as_view(), name='registrar_pago'),
    path('<int:orden_pk>/editar-servicio/<int:pk>/', views.EditarServicioView.as_view(), name='editar_servicio'),
    path('<int:orden_pk>/eliminar-servicio/<int:pk>/', views.EliminarServicioView.as_view(), name='eliminar_servicio'),
    path('<int:orden_pk>/editar-repuesto/<int:pk>/', views.EditarRepuestoView.as_view(), name='editar_repuesto'),
    path('<int:orden_pk>/eliminar-repuesto/<int:pk>/', views.EliminarRepuestoView.as_view(), name='eliminar_repuesto'),
]
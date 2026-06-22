from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.RepuestoListView.as_view(), name='repuesto_list'),
    path('nuevo/', views.RepuestoCreateView.as_view(), name='repuesto_create'),
    path('<int:pk>/', views.RepuestoDetailView.as_view(), name='repuesto_detail'),
    path('<int:pk>/editar/', views.RepuestoUpdateView.as_view(), name='repuesto_update'),
    path('ajuste/', views.AjusteStockView.as_view(), name='ajuste_stock'),
    path('movimientos/', views.MovimientoListView.as_view(), name='movimiento_list'),
]
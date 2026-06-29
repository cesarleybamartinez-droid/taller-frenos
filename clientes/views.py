from urllib import request

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db.models import Q
from .models import Cliente, Vehiculo
from .forms import ClienteForm, VehiculoForm
from core.mixins import TienePermisoMixin
from django.http import JsonResponse
from .models import ModeloVehiculo
from core.mixins import TienePermisoMixin, OrdenYPaginacionMixin
from django.db.models import Q

def get_modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    if marca_id:
        modelos = ModeloVehiculo.objects.filter(marca_id=marca_id).values('id', 'nombre')
        return JsonResponse(list(modelos), safe=False)
    return JsonResponse([], safe=False)

# --- Vistas de Cliente ---
class ClienteListView(LoginRequiredMixin, OrdenYPaginacionMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    ordering_allowed = {'nombre': 'nombre', 'telefono': 'telefono', 'cedula': 'cedula'}
    ordering_default = 'nombre'

    def get_queryset(self):
        queryset = Cliente.objects.all()
        # Filtro activos/inactivos
        filtro_activo = self.request.GET.get('activo', 'activos')
        if filtro_activo == 'activos':
            queryset = queryset.filter(activo=True)
        elif filtro_activo == 'inactivos':
            queryset = queryset.filter(activo=False)
        # Búsqueda
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(telefono__icontains=search) |
                Q(cedula__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['filtro_activo'] = self.request.GET.get('activo', 'activos')
        context['per_page'] = self.request.GET.get('per_page', '20')
        return context


class ClienteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Crea un nuevo cliente y muestra un mensaje de éxito."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')
    success_message = "Cliente creado exitosamente."


class ClienteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Actualiza un cliente existente y muestra un mensaje de éxito."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')
    success_message = "Cliente actualizado exitosamente."


class ClienteDetailView(LoginRequiredMixin, DetailView):
    """Muestra el detalle de un cliente y sus vehículos."""
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculos'] = self.object.vehiculos.filter(activo=True)
        return context


class ClienteDeleteView(LoginRequiredMixin, TienePermisoMixin, UpdateView):
    permiso = 'desactivar_usuario'
    """Desactiva un cliente (eliminación lógica) y muestra un mensaje."""
    model = Cliente
    fields = []
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def form_valid(self, form):
        messages.success(self.request, "Cliente desactivado exitosamente.")
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)


# --- Vistas de Vehículo ---

class VehiculoListView(LoginRequiredMixin, OrdenYPaginacionMixin, ListView):
    model = Vehiculo
    template_name = 'clientes/vehiculo_list.html'
    context_object_name = 'vehiculos'
    ordering_allowed = {'placa': 'placa', 'marca__nombre': 'marca__nombre', 'modelo__nombre': 'modelo__nombre', 'anio': 'anio'}
    ordering_default = 'placa'

    def get_queryset(self):
        queryset = Vehiculo.objects.filter(activo=True).select_related('cliente', 'marca', 'modelo')
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(placa__icontains=search) |
                Q(cliente__nombre__icontains=search)
            )
        return queryset


class VehiculoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Crea un nuevo vehículo y muestra un mensaje de éxito."""
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'clientes/vehiculo_form.html'
    success_url = reverse_lazy('clientes:vehiculo_list')
    success_message = "Vehículo registrado exitosamente."


class VehiculoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Actualiza un vehículo existente y muestra un mensaje de éxito."""
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'clientes/vehiculo_form.html'
    success_url = reverse_lazy('clientes:vehiculo_list')
    success_message = "Vehículo actualizado exitosamente."


class VehiculoDetailView(LoginRequiredMixin, DetailView):
    """Muestra el detalle de un vehículo."""
    model = Vehiculo
    template_name = 'clientes/vehiculo_detail.html'
    context_object_name = 'vehiculo'


class VehiculoDeleteView(LoginRequiredMixin, TienePermisoMixin, UpdateView):
    """Desactiva un vehículo (eliminación lógica) y muestra un mensaje."""
    permiso = 'desactivar_usuario'
    model = Vehiculo
    fields = []
    template_name = 'clientes/vehiculo_confirm_delete.html'
    success_url = reverse_lazy('clientes:vehiculo_list')

    def form_valid(self, form):
        messages.success(self.request, "Vehículo desactivado exitosamente.")
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)
    
    def get_modelos_por_marca(request):
        marca_id = request.GET.get('marca_id')
        if marca_id:
            modelos = ModeloVehiculo.objects.filter(marca_id=marca_id).values('id', 'nombre')
        return JsonResponse(list(modelos), safe=False)
        return JsonResponse([], safe=False)
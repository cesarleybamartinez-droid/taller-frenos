from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Cliente, Vehiculo
from .forms import ClienteForm, VehiculoForm

# Mixin para restringir acciones a Admin/Propietario
class SoloAdminPropietarioMixin:
    def test_func(self):
        return self.request.user.rol.nombre in ['Propietario', 'Administrador']

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Cliente.objects.filter(activo=True)
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(telefono__icontains=search) |
                Q(cedula__icontains=search)
            )
        return queryset

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculos'] = self.object.vehiculos.filter(activo=True)
        return context

class ClienteDeleteView(LoginRequiredMixin, SoloAdminPropietarioMixin, UpdateView):
    model = Cliente
    fields = []
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def form_valid(self, form):
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)

# Vistas de Vehículo (similar)
class VehiculoListView(LoginRequiredMixin, ListView):
    model = Vehiculo
    template_name = 'clientes/vehiculo_list.html'
    context_object_name = 'vehiculos'
    paginate_by = 20

class VehiculoCreateView(LoginRequiredMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'clientes/vehiculo_form.html'
    success_url = reverse_lazy('clientes:vehiculo_list')

class VehiculoUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'clientes/vehiculo_form.html'
    success_url = reverse_lazy('clientes:vehiculo_list')

class VehiculoDetailView(LoginRequiredMixin, DetailView):
    model = Vehiculo
    template_name = 'clientes/vehiculo_detail.html'

class VehiculoDeleteView(LoginRequiredMixin, SoloAdminPropietarioMixin, UpdateView):
    model = Vehiculo
    fields = []
    template_name = 'clientes/vehiculo_confirm_delete.html'
    success_url = reverse_lazy('clientes:vehiculo_list')

    def form_valid(self, form):
        self.object.activo = False
        self.object.save()
        return super().form_valid(form)
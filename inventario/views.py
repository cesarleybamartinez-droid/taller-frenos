from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from core.mixins import TienePermisoMixin
from .models import Repuesto, MovimientoInventario
from .forms import RepuestoForm, AjusteStockForm


class RepuestoListView(LoginRequiredMixin, ListView):
    """Lista de repuestos con alerta de stock bajo."""
    model = Repuesto
    template_name = 'inventario/repuesto_list.html'
    context_object_name = 'repuestos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Repuesto.objects.select_related('categoria').all()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(descripcion__icontains=search) | queryset.filter(codigo__icontains=search)
        return queryset


class RepuestoCreateView(LoginRequiredMixin, TienePermisoMixin, SuccessMessageMixin, CreateView):
    """Crear un nuevo repuesto (solo Admin/Prop)."""
    permiso = 'gestionar_inventario'
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'inventario/repuesto_form.html'
    success_url = reverse_lazy('inventario:repuesto_list')
    success_message = "Repuesto creado exitosamente."


class RepuestoUpdateView(LoginRequiredMixin, TienePermisoMixin, SuccessMessageMixin, UpdateView):
    """Editar un repuesto existente (solo Admin/Prop)."""
    permiso = 'gestionar_inventario'
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'inventario/repuesto_form.html'
    success_url = reverse_lazy('inventario:repuesto_list')
    success_message = "Repuesto actualizado exitosamente."


class RepuestoDetailView(LoginRequiredMixin, DetailView):
    """Ver detalle de un repuesto y su historial de movimientos."""
    model = Repuesto
    template_name = 'inventario/repuesto_detail.html'
    context_object_name = 'repuesto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimientos'] = self.object.movimientoinventario_set.all()[:30]
        return context


class AjusteStockView(LoginRequiredMixin, TienePermisoMixin, SuccessMessageMixin, CreateView):
    """Realizar un ajuste manual de stock (solo Admin/Prop)."""
    permiso = 'gestionar_inventario'
    model = MovimientoInventario
    form_class = AjusteStockForm
    template_name = 'inventario/ajuste_stock.html'
    success_url = reverse_lazy('inventario:repuesto_list')
    success_message = "Ajuste de stock realizado exitosamente."

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        repuesto = form.cleaned_data['repuesto']
        cantidad = form.cleaned_data['cantidad']
        tipo = form.cleaned_data['tipo']

        if tipo == 'Entrada':
            repuesto.stock_actual += cantidad
        elif tipo == 'Salida':
            if repuesto.stock_actual < cantidad:
                form.add_error('cantidad', 'No hay suficiente stock para esta salida.')
                return self.form_invalid(form)
            repuesto.stock_actual -= cantidad
        elif tipo == 'Ajuste':
            repuesto.stock_actual = cantidad

        repuesto.save()
        return super().form_valid(form)


class MovimientoListView(LoginRequiredMixin, ListView):
    """Historial completo de movimientos de inventario."""
    model = MovimientoInventario
    template_name = 'inventario/movimiento_list.html'
    context_object_name = 'movimientos'
    paginate_by = 50
    ordering = ['-fecha']
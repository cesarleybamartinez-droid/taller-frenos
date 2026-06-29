from urllib import response
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, models as db_models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, FormView, DeleteView
from core.mixins import TienePermisoMixin
from .models import OrdenTrabajo, DetalleServicio, DetalleRepuesto, Pago, Servicio
from inventario.models import Repuesto, MovimientoInventario
from django.http import JsonResponse
from .models import Servicio
from core.mixins import TienePermisoMixin, OrdenYPaginacionMixin
from django.db.models import Q
from .forms import (
    OrdenTrabajoForm,
    DetalleServicioForm,
    DetalleRepuestoForm,
    PagoForm,
    CambioEstadoForm,
    EditarServicioForm, EditarRepuestoForm
)


# --- LISTA DE ÓRDENES ---
class OrdenListView(LoginRequiredMixin, OrdenYPaginacionMixin, ListView):
    model = OrdenTrabajo
    template_name = 'ordenes/orden_list.html'
    context_object_name = 'ordenes'
    ordering_allowed = {'id': 'id', 'fecha_ingreso': 'fecha_ingreso', 'total': 'total', 'estado': 'estado'}
    ordering_default = '-fecha_ingreso'

    def get_queryset(self):
        queryset = OrdenTrabajo.objects.select_related('vehiculo__cliente').all()
        estado = self.request.GET.get('estado', '')
        fecha_inicio = self.request.GET.get('fecha_inicio', '')
        fecha_fin = self.request.GET.get('fecha_fin', '')
        search = self.request.GET.get('search', '')
        if estado:
            queryset = queryset.filter(estado=estado)
        if fecha_inicio:
            queryset = queryset.filter(fecha_ingreso__date__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_ingreso__date__lte=fecha_fin)
        if search:
            queryset = queryset.filter(
                Q(vehiculo__placa__icontains=search) |
                Q(vehiculo__cliente__nombre__icontains=search)
            )
        return queryset


# --- CREAR ORDEN ---
class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = OrdenTrabajo
    form_class = OrdenTrabajoForm
    template_name = 'ordenes/orden_form.html'
    success_url = reverse_lazy('ordenes:orden_list')

    def form_valid(self, form):
        form.instance.estado = 'Pendiente'
        return super().form_valid(form)


# --- DETALLE DE ORDEN ---
class OrdenDetailView(LoginRequiredMixin, DetailView):
    model = OrdenTrabajo
    template_name = 'ordenes/orden_detail.html'
    context_object_name = 'orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles_servicios'] = self.object.detalleservicio_set.select_related('servicio').all()
        context['detalles_repuestos'] = self.object.detallerepuesto_set.select_related('repuesto').all()
        context['pagos'] = self.object.pago_set.all()
        context['saldo_pendiente'] = self.object.saldo_pendiente
        context['puede_editar'] = self.object.estado not in ['Entregada', 'Cancelada']
        return context


# --- AGREGAR SERVICIO A LA ORDEN ---
class AgregarServicioView(LoginRequiredMixin, CreateView):
    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'ordenes/agregar_servicio.html'

    def form_valid(self, form):
        orden = get_object_or_404(OrdenTrabajo, pk=self.kwargs['orden_pk'])
        if orden.estado in ['Entregada', 'Cancelada']:
            messages.error(self.request, "No se puede modificar una orden cerrada.")
            return redirect('ordenes:orden_detail', pk=orden.pk)
        form.instance.orden = orden
        form.instance.subtotal = form.cleaned_data['cantidad'] * form.cleaned_data['precio_unitario']
        response = super().form_valid(form)
        self._actualizar_totales(orden)
        return response

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.kwargs['orden_pk']})

    def _actualizar_totales(self, orden):
        orden.subtotal_servicios = orden.detalleservicio_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.subtotal_repuestos = orden.detallerepuesto_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()


# --- AGREGAR REPUESTO A LA ORDEN ---
class AgregarRepuestoView(LoginRequiredMixin, CreateView):
    model = DetalleRepuesto
    form_class = DetalleRepuestoForm
    template_name = 'ordenes/agregar_repuesto.html'

    def form_valid(self, form):
        orden = get_object_or_404(OrdenTrabajo, pk=self.kwargs['orden_pk'])
        if orden.estado in ['Entregada', 'Cancelada']:
            messages.error(self.request, "No se puede modificar una orden cerrada.")
            return redirect('ordenes:orden_detail', pk=orden.pk)
        repuesto = form.cleaned_data['repuesto']
        cantidad = form.cleaned_data['cantidad']
        if repuesto.stock_actual < cantidad:
            form.add_error('cantidad', f'Stock insuficiente. Disponible: {repuesto.stock_actual}')
            return self.form_invalid(form)
        with transaction.atomic():
            repuesto.stock_actual -= cantidad
            repuesto.save()
            MovimientoInventario.objects.create(
                repuesto=repuesto, tipo='Salida', cantidad=cantidad,
                motivo=f'Usado en orden #{orden.pk}', usuario=self.request.user
            )
            form.instance.orden = orden
            form.instance.precio_unitario = repuesto.precio_venta
            form.instance.costo_unitario = repuesto.costo_unitario
            form.instance.subtotal = cantidad * repuesto.precio_venta
            response = super().form_valid(form)
            self._actualizar_totales(orden)
        return response

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.kwargs['orden_pk']})

    def _actualizar_totales(self, orden):
        orden.subtotal_servicios = orden.detalleservicio_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.subtotal_repuestos = orden.detallerepuesto_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()


# --- CAMBIAR ESTADO ---
class CambiarEstadoView(LoginRequiredMixin, FormView):
    """Vista para cambiar el estado de una orden."""
    form_class = CambioEstadoForm
    template_name = 'ordenes/cambiar_estado.html'

    def get_estados_permitidos(self, orden, usuario):
        rol = usuario.rol.nombre if usuario.rol else ''
        flujo = {
            'Pendiente': ['Diagnóstico', 'Cancelada'],
            'Diagnóstico': ['Esperando Aprobación', 'En Progreso', 'Cancelada'],
            'Esperando Aprobación': ['En Progreso', 'Cancelada'],
            'En Progreso': ['Suspendida', 'Finalizada'],
            'Suspendida': ['En Progreso', 'Cancelada'],
            'Finalizada': ['Entregada'],
        }
        permitidos = flujo.get(orden.estado, [])
        if rol == 'Recepcionista':
            permitidos = [e for e in permitidos if e in ['Diagnóstico', 'En Progreso']]
        elif rol == 'Administrador':
            permitidos = [e for e in permitidos if e not in ['Cancelada']]
        if orden.estado in ['Entregada', 'Cancelada']:
            permitidos = []
        return permitidos

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        orden = get_object_or_404(OrdenTrabajo, pk=self.kwargs['pk'])
        kwargs['estados_permitidos'] = self.get_estados_permitidos(orden, self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = get_object_or_404(OrdenTrabajo, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        nuevo_estado = form.cleaned_data['estado']
        orden = get_object_or_404(OrdenTrabajo, pk=self.kwargs['pk'])

        if nuevo_estado == 'Entregada':
            if orden.saldo_pendiente > 0:
                messages.error(self.request, "No se puede entregar: hay saldo pendiente.")
                return self.form_invalid(form)
            orden.fecha_entrega_real = timezone.now()

        orden.estado = nuevo_estado
        orden.save()
        messages.success(self.request, f"Orden #{orden.pk} pasó a estado: {nuevo_estado}")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.kwargs['pk']})

# --- REGISTRAR PAGO ---
class RegistrarPagoView(LoginRequiredMixin, CreateView):
    """Registrar un pago para una orden."""
    model = Pago
    form_class = PagoForm
    template_name = 'ordenes/registrar_pago.html'

    def get_initial(self):
        initial = super().get_initial()
        orden = get_object_or_404(OrdenTrabajo, pk=self.kwargs['orden_pk'])
        initial['monto'] = orden.saldo_pendiente
        return initial
    
    def form_valid(self, form):
        orden = get_object_or_404(OrdenTrabajo, pk=self.kwargs['orden_pk'])
        form.instance.orden = orden
        monto = form.cleaned_data['monto']
        if monto > orden.saldo_pendiente:
            form.add_error('monto', f'El monto supera el saldo pendiente (RD$ {orden.saldo_pendiente})')
            return self.form_invalid(form)
        response = super().form_valid(form)
        if orden.saldo_pendiente == 0 and orden.estado == 'Finalizada':
            orden.estado = 'Entregada'
            orden.fecha_entrega_real = timezone.now()
            orden.save()
            messages.success(self.request, "Pago completo. La orden ha sido marcada como Entregada.")
        else:
            messages.success(self.request, f"Pago registrado. Saldo pendiente: RD$ {orden.saldo_pendiente}")
        return response

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.kwargs['orden_pk']})

# -------------------------------------------------------
# EDITAR Y ELIMINAR SERVICIOS
# -------------------------------------------------------
class EditarServicioView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DetalleServicio
    form_class = EditarServicioForm
    template_name = 'ordenes/editar_servicio.html'
    success_message = "Servicio actualizado correctamente."

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.object.orden_id})

    def dispatch(self, request, *args, **kwargs):
        detalle = self.get_object()
        if detalle.orden.estado in ['Entregada', 'Cancelada']:
            messages.error(request, "No se puede modificar una orden cerrada.")
            return redirect('ordenes:orden_detail', pk=detalle.orden_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        detalle = self.object
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario
        response = super().form_valid(form)
        orden = detalle.orden
        self._actualizar_totales(orden)
        return response

    def _actualizar_totales(self, orden):
        orden.subtotal_servicios = orden.detalleservicio_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.subtotal_repuestos = orden.detallerepuesto_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()


class EliminarServicioView(LoginRequiredMixin, DeleteView):
    model = DetalleServicio
    template_name = 'ordenes/eliminar_servicio.html'

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.kwargs['orden_pk']})

    def dispatch(self, request, *args, **kwargs):
        detalle = self.get_object()
        if detalle.orden.estado in ['Entregada', 'Cancelada']:
            messages.error(request, "No se puede modificar una orden cerrada.")
            return redirect('ordenes:orden_detail', pk=detalle.orden_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        orden = self.object.orden
        self.object.delete()
        self._actualizar_totales(orden)
        messages.success(self.request, "Servicio eliminado correctamente.")
        return HttpResponseRedirect(self.get_success_url())

    def _actualizar_totales(self, orden):
        orden.subtotal_servicios = orden.detalleservicio_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.subtotal_repuestos = orden.detallerepuesto_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()


# -------------------------------------------------------
# EDITAR Y ELIMINAR REPUESTOS
# -------------------------------------------------------
class EditarRepuestoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DetalleRepuesto
    form_class = EditarRepuestoForm
    template_name = 'ordenes/editar_repuesto.html'
    success_message = "Repuesto actualizado correctamente."

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.object.orden_id})

    def dispatch(self, request, *args, **kwargs):
        detalle = self.get_object()
        if detalle.orden.estado in ['Entregada', 'Cancelada']:
            messages.error(request, "No se puede modificar una orden cerrada.")
            return redirect('ordenes:orden_detail', pk=detalle.orden_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        detalle = self.object
        nueva_cantidad = form.cleaned_data['cantidad']
        cantidad_anterior = detalle.cantidad
        repuesto = detalle.repuesto
        diferencia = nueva_cantidad - cantidad_anterior

        with transaction.atomic():
            if diferencia > 0:
                if repuesto.stock_actual < diferencia:
                    form.add_error('cantidad', f'Stock insuficiente. Disponible: {repuesto.stock_actual}')
                    return self.form_invalid(form)
                repuesto.stock_actual -= diferencia
                MovimientoInventario.objects.create(
                    repuesto=repuesto, tipo='Salida', cantidad=diferencia,
                    motivo=f'Ajuste en orden #{detalle.orden_id} (aumento)', usuario=self.request.user
                )
            elif diferencia < 0:
                repuesto.stock_actual += abs(diferencia)
                MovimientoInventario.objects.create(
                    repuesto=repuesto, tipo='Entrada', cantidad=abs(diferencia),
                    motivo=f'Ajuste en orden #{detalle.orden_id} (disminución)', usuario=self.request.user
                )

            repuesto.save()
            detalle.subtotal = nueva_cantidad * detalle.precio_unitario
            response = super().form_valid(form)

            orden = detalle.orden
            self._actualizar_totales(orden)
        return response

    def _actualizar_totales(self, orden):
        orden.subtotal_servicios = orden.detalleservicio_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.subtotal_repuestos = orden.detallerepuesto_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()


class EliminarRepuestoView(LoginRequiredMixin, DeleteView):
    model = DetalleRepuesto
    template_name = 'ordenes/eliminar_repuesto.html'

    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.kwargs['orden_pk']})

    def dispatch(self, request, *args, **kwargs):
        detalle = self.get_object()
        if detalle.orden.estado in ['Entregada', 'Cancelada']:
            messages.error(request, "No se puede modificar una orden cerrada.")
            return redirect('ordenes:orden_detail', pk=detalle.orden_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        detalle = self.object
        repuesto = detalle.repuesto
        orden = detalle.orden

        with transaction.atomic():
            repuesto.stock_actual += detalle.cantidad
            repuesto.save()
            MovimientoInventario.objects.create(
                repuesto=repuesto, tipo='Entrada', cantidad=detalle.cantidad,
                motivo=f'Reintegro por eliminación en orden #{orden.pk}', usuario=self.request.user
            )
            detalle.delete()
            self._actualizar_totales(orden)
        messages.success(self.request, "Repuesto eliminado correctamente. Stock reintegrado.")
        return HttpResponseRedirect(self.get_success_url())

    def _actualizar_totales(self, orden):
        orden.subtotal_servicios = orden.detalleservicio_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.subtotal_repuestos = orden.detallerepuesto_set.aggregate(t=db_models.Sum('subtotal'))['t'] or 0
        orden.total = orden.subtotal_servicios + orden.subtotal_repuestos - orden.descuento
        orden.itbis = orden.total * Decimal('0.18')
        orden.total += orden.itbis
        orden.save()
    
def get_precio_servicio(request):
    servicio_id = request.GET.get('servicio_id')
    if servicio_id:
        try:
            servicio = Servicio.objects.get(pk=servicio_id)
            return JsonResponse({'precio': str(servicio.precio_estandar)})
        except Servicio.DoesNotExist:
            pass
    return JsonResponse({'precio': '0.00'})
        
    def get_success_url(self):
        return reverse('ordenes:orden_detail', kwargs={'pk': self.kwargs['orden_pk']})
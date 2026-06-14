from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from core.models import Usuario
from seguridad.models import Auditoria, Rol, Permiso, RolPermiso
from .forms import UsuarioForm, RolPermisoForm
from core.mixins import TienePermisoMixin


class UsuarioListView(LoginRequiredMixin, TienePermisoMixin, ListView):
    """Lista de usuarios del sistema."""
    permiso = 'ver_auditoria'   # o podrías crear un permiso específico 'ver_usuarios'
    model = Usuario
    template_name = 'seguridad/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos los roles para la pestaña "Roles"
        context['roles'] = Rol.objects.all()
        return context

class UsuarioCreateView(LoginRequiredMixin, TienePermisoMixin, SuccessMessageMixin, CreateView):
    """Crear un nuevo usuario."""
    permiso = 'crear_usuario'
    model = Usuario
    form_class = UsuarioForm
    template_name = 'seguridad/usuario_form.html'
    success_url = reverse_lazy('seguridad:usuario_list')
    success_message = "Usuario creado exitosamente."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['rol'].queryset = Rol.objects.all()
        return form


class UsuarioUpdateView(LoginRequiredMixin, TienePermisoMixin, SuccessMessageMixin, UpdateView):
    """Editar un usuario existente."""
    permiso = 'editar_usuario'
    model = Usuario
    form_class = UsuarioForm
    template_name = 'seguridad/usuario_form.html'
    success_url = reverse_lazy('seguridad:usuario_list')
    success_message = "Usuario actualizado exitosamente."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['rol'].queryset = Rol.objects.all()
        return form


class AuditoriaListView(LoginRequiredMixin, TienePermisoMixin, ListView):
    """Lista de registros de auditoría."""
    permiso = 'ver_auditoria'
    model = Auditoria
    template_name = 'seguridad/auditoria_list.html'
    context_object_name = 'registros'
    paginate_by = 50
    ordering = ['-fecha_hora']

    def get_queryset(self):
        queryset = super().get_queryset()
        accion = self.request.GET.get('accion', '')
        fecha_inicio = self.request.GET.get('fecha_inicio', '')
        fecha_fin = self.request.GET.get('fecha_fin', '')
        if accion:
            queryset = queryset.filter(accion__icontains=accion)
        if fecha_inicio:
            queryset = queryset.filter(fecha_hora__date__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_hora__date__lte=fecha_fin)
        return queryset
    
class UsuarioDeleteView(LoginRequiredMixin, TienePermisoMixin, UpdateView):
    """Desactiva un usuario (eliminación lógica) y muestra un mensaje."""
    permiso = 'desactivar_usuario'
    model = Usuario
    fields = []  # No necesitamos formulario, solo confirmación
    template_name = 'seguridad/usuario_confirm_delete.html'
    success_url = reverse_lazy('seguridad:usuario_list')

    def form_valid(self, form):
        if self.object == self.request.user:
            messages.error(self.request, "No puedes desactivar tu propio usuario.")
            return redirect(self.success_url)
        messages.success(self.request, f"Usuario {self.object.username} desactivado exitosamente.")
        self.object.is_active = False
        self.object.save()
        return super().form_valid(form)
class RolListView(LoginRequiredMixin, TienePermisoMixin, ListView):
    """Lista de roles del sistema (solo Propietario con permiso)."""
    permiso = 'gestionar_permisos'
    model = Rol
    template_name = 'seguridad/rol_list.html'
    context_object_name = 'roles'


class RolPermisoUpdateView(LoginRequiredMixin, TienePermisoMixin, FormView):
    """Permite editar los permisos de un rol específico."""
    permiso = 'gestionar_permisos'
    form_class = RolPermisoForm
    template_name = 'seguridad/rol_permisos.html'
    success_url = reverse_lazy('seguridad:rol_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['rol'] = Rol.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        # Agregamos el rol al contexto para usarlo en la plantilla
        context = super().get_context_data(**kwargs)
        context['rol'] = Rol.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        form.rol = Rol.objects.get(pk=self.kwargs['pk'])
        form.save()
        messages.success(self.request, "Permisos actualizados correctamente.")
        return super().form_valid(form)
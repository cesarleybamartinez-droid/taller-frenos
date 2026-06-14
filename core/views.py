from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    """Vista de inicio de sesión personalizada."""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('clientes:cliente_list')


def cerrar_sesion(request):
    """Cierra la sesión del usuario y lo redirige al login."""
    logout(request)
    return redirect('/login/')
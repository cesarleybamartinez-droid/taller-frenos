from django import forms
from .models import Cliente, Vehiculo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'cedula', 'correo', 'direccion']

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'placa', 'marca', 'modelo', 'anio', 'color', 'chasis', 'tipo_frenos']
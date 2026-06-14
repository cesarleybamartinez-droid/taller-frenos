from django import forms
from .models import Cliente, Vehiculo

class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes."""
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'cedula', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '809-xxx-xxxx'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '001-xxxxxxx-x'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dirección'}),
        }
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
            'cedula': 'Cédula',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
        }

    def clean_telefono(self):
        """Valida que el teléfono no esté duplicado."""
        telefono = self.cleaned_data.get('telefono')
        if Cliente.objects.filter(telefono=telefono).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este teléfono ya está registrado.")
        return telefono


class VehiculoForm(forms.ModelForm):
    """Formulario para crear y editar vehículos."""
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'placa', 'marca', 'modelo', 'anio', 'color', 'chasis', 'tipo_frenos']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'chasis': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_frenos': forms.Select(attrs={'class': 'form-control'}),
        }
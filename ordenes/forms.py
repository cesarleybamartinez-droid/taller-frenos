from django import forms
from .models import OrdenTrabajo, DetalleServicio, DetalleRepuesto, Pago


class OrdenTrabajoForm(forms.ModelForm):
    """Formulario para crear la cabecera de la orden."""
    class Meta:
        model = OrdenTrabajo
        fields = ['vehiculo', 'diagnostico', 'observaciones', 'fecha_estimada_entrega']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describa el problema o diagnóstico'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observaciones adicionales'}),
            'fecha_estimada_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'vehiculo': 'Vehículo',
            'diagnostico': 'Diagnóstico / Problema',
            'observaciones': 'Observaciones',
            'fecha_estimada_entrega': 'Fecha estimada de entrega',
        }


class DetalleServicioForm(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['servicio', 'cantidad', 'precio_unitario']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-control', 'id': 'id_servicio'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_precio_unitario'}),
        }
        labels = {
            'servicio': 'Servicio',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio unitario (RD$)',
        }


class DetalleRepuestoForm(forms.ModelForm):
    """Formulario para agregar un repuesto a la orden."""
    class Meta:
        model = DetalleRepuesto
        fields = ['repuesto', 'cantidad']
        widgets = {
            'repuesto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'repuesto': 'Repuesto',
            'cantidad': 'Cantidad',
        }


class PagoForm(forms.ModelForm):
    """Formulario para registrar un pago."""
    class Meta:
        model = Pago
        fields = ['monto', 'metodo']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'monto': 'Monto (RD$)',
            'metodo': 'Método de pago',
        }


class CambioEstadoForm(forms.Form):
    """Formulario simple para cambiar el estado de una orden."""
    estado = forms.ChoiceField(
        choices=[],  # Se llena dinámicamente en la vista
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Nuevo estado'
    )

    def __init__(self, *args, **kwargs):
        estados_permitidos = kwargs.pop('estados_permitidos', [])
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [(e, e) for e in estados_permitidos]
        
class EditarServicioForm(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['cantidad', 'precio_unitario']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class EditarRepuestoForm(forms.ModelForm):
    class Meta:
        model = DetalleRepuesto
        fields = ['cantidad', 'precio_unitario']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }       
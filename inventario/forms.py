from django import forms
from .models import Repuesto, MovimientoInventario, CategoriaRepuesto


class RepuestoForm(forms.ModelForm):
    """Formulario para crear o editar un repuesto."""
    class Meta:
        model = Repuesto
        fields = ['codigo', 'descripcion', 'marca', 'categoria', 'costo_unitario', 'precio_venta', 'stock_actual', 'stock_minimo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'costo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'marca': 'Marca',
            'categoria': 'Categoría',
            'costo_unitario': 'Costo unitario (RD$)',
            'precio_venta': 'Precio de venta (RD$)',
            'stock_actual': 'Stock actual',
            'stock_minimo': 'Stock mínimo',
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if Repuesto.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este código ya está registrado.")
        return codigo


class AjusteStockForm(forms.ModelForm):
    """Formulario para realizar un ajuste manual de stock."""
    class Meta:
        model = MovimientoInventario
        fields = ['repuesto', 'tipo', 'cantidad', 'motivo']
        widgets = {
            'repuesto': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'repuesto': 'Repuesto',
            'tipo': 'Tipo de movimiento',
            'cantidad': 'Cantidad',
            'motivo': 'Motivo',
        }
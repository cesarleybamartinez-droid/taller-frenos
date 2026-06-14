from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Usuario
from seguridad.models import Rol, Permiso, RolPermiso


class UsuarioForm(forms.ModelForm):
    """Formulario para crear o editar usuarios."""
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Dejar en blanco para mantener la contraseña actual."
    )
    # Campo adicional de solo lectura para mostrar los permisos del rol seleccionado
    permisos_heredados = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled', 'class': 'form-check-input'}),
        label='Permisos del rol',
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'rol', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'rol': 'Rol',
            'is_active': 'Activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.all()

        # Si estamos editando un usuario existente, mostrar los permisos de su rol
        if self.instance and self.instance.pk and self.instance.rol:
            self.fields['permisos_heredados'].initial = self.instance.rol.rolpermiso_set.values_list('permiso_id', flat=True)
        else:
            # Para creación, dejarlo vacío (se podría llenar dinámicamente con JS)
            self.fields['permisos_heredados'].initial = []

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class RolPermisoForm(forms.Form):
    """Formulario para editar los permisos de un rol."""
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Permisos asignados',
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.rol = kwargs.pop('rol', None)
        super().__init__(*args, **kwargs)
        if self.rol:
            self.fields['permisos'].initial = self.rol.rolpermiso_set.values_list('permiso_id', flat=True)

    def save(self):
        self.rol.rolpermiso_set.all().delete()
        for permiso in self.cleaned_data['permisos']:
            RolPermiso.objects.create(rol=self.rol, permiso=permiso)
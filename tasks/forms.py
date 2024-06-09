from django import forms
from .models import UsuarioComun

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UsuarioComun
        fields = ['nombre', 'edad', 'fecha_nacimiento', 'telefono', 'direccion']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


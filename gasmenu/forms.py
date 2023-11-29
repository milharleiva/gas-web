from django import forms
from .models import Solicitud
from django.contrib.auth.models import User
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['rut', 'nombre', 'apellidos', 'direccion', 'telefono', 'comuna', 'estado']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

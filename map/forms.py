from django import forms
from .models import Muestreo


class DatosForm(forms.ModelForm):
    class Meta:
        model = Muestreo
        fields = ['nro_vuelo', 'latitud', 'longitud', 'direccion', 'fecha_muestreo']
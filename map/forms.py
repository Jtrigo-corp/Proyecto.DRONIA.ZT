# forms.py
from django import forms
from .models import Imagenes

class DatosForm(forms.ModelForm):
    class Meta:
        model = Imagenes
        fields = ['vuelo', 'nombre_imagen']

    def __init__(self, vuelos, *args, **kwargs):
        super(DatosForm, self).__init__(*args, **kwargs)
        self.fields['vuelo'].queryset = vuelos

from .models import Vuelo

class IngresarVueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ['sector_vuelo', 'fecha_vuelo']

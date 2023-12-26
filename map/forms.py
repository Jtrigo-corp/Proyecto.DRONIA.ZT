from django import forms
from .models import AreaMuestreo, Vuelo, Imagenes  # Importa Vuelo aquí

class AreaMuestreoForm(forms.ModelForm):
    class Meta:
        model = AreaMuestreo
        fields = ['direccion', 'latitud', 'longitud']   
class DatosForm(forms.ModelForm):
    class Meta:
        model = Imagenes
        fields = ['vuelo', 'nombre_imagen']

    def __init__(self, *args, **kwargs):
        vuelos = kwargs.pop('vuelos', None)
        super(DatosForm, self).__init__(*args, **kwargs)
        if vuelos is not None:
            self.fields['vuelo'].queryset = vuelos

class IngresarVueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ['sector_vuelo', 'fecha_vuelo']
        
     
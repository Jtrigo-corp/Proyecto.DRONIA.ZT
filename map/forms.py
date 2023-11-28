from django import forms
from .models import Muestreo


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
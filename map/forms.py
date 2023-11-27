from django import forms
from .models import ImageData

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageData
        fields = ['image', 'latitude', 'longitude', 'address', 'flight_number']
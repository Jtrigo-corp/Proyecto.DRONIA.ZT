from django.core.files.storage import FileSystemStorage

from django.conf import settings
from map.forms import ImageUploadForm
from .models import ImageData
import requests
from django.utils import timezone
import logging
logging.getLogger('sagemaker').setLevel(logging.WARNING)
from sagemaker import Predictor
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import folium
from rest_framework import views, response

from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import folium
from map.models import Vuelo
from rest_framework import views, response
from api.serializers import *

from django.contrib.auth.decorators import login_required

from map.models import Ubicacion

def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "pages/index.html", context)

def ubicacion(request):
  ubicaciones = Ubicacion.objects.all()
  initialMap = folium.Map(location=[-27.370371, -70.322529], zoom_start=13.5)
  context = {
    'segment'  : 'ubicacion',
    'home' : initialMap._repr_html_(),
    #'products' : Product.objects.all()
  }
  return render(request, "pages/ubicacion.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context), 

def carga(request):
  context = {
    'segment': 'carga'
  }
  return render(request, "pages/carga.html", context)

def mapanalisis(request):
  context = {
    'segment': 'mapanalisis'
  }
  return render(request, "pages/mapanalisis.html", context)


def list_vuelos(request):
  vuelos = list(Vuelo.objects.values())
  data = {'vuelos': vuelos}
  return JsonResponse(data)

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = form.save(commit=False)
            # Almacena la imagen en Azure Blob Storage
            image_data.save()

            # Llama a la API de Custom Vision para análisis
            analyze_image(image_data)

            return redirect('upload_success')
    else:
        form = ImageUploadForm()
    return render(request, 'cargar_imagen.html', {'form': form})


def analyze_images(request):
    images = ImageData.objects.all().order_by('-upload_date')[:10]
    return render(request, 'analyze_images.html', {'images': images})

def analyze_image(request):
    if request.method == 'POST' and 'image_id' in request.POST:
        image_id = request.POST['image_id']
        try:
            image_data = ImageData.objects.get(id=image_id)
            # Llama a la función de análisis que implementaste previamente
            analyze_image(image_data)
            # Devuelve resultados para actualizar el DataTable de resultados de análisis
            response_data = {
                'image_url': image_data.image.url,
                'detected_tree_type': image_data.detected_tree_type,
                'confidence': image_data.confidence,
                'analysis_date': image_data.analysis_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(response_data)
        except ImageData.DoesNotExist:
            return JsonResponse({'error': 'La imagen no existe'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'})

def analyze_image(image_data):
    # Configuración de la API de Custom Vision
    custom_vision_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/ac1a4186-aebf-4acb-8542-e385462fa36d/classify/iterations/Modelo-6-allclass/image"  # Reemplaza con la URL de punto de conexión de Custom Vision
    custom_vision_key = "8a2c550f6e454de4885bd5a49644f572"  # Reemplaza con la clave de predicción del modelo

    # Configuración de la solicitud
    headers = {
        "Content-Type": "application/octet-stream",
        "Prediction-Key": custom_vision_key
    }

    # Ruta local de la imagen en el servidor
    image_path = image_data.image.path

    # Lectura de la imagen como bytes
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Realizar la solicitud a la API de Custom Vision
    response = requests.post(custom_vision_url, headers=headers, data=image_data)

    # Manejar la respuesta
    if response.status_code == 200:
        result = response.json()
        # Extraer información relevante de la respuesta de Custom Vision
        predicted_tree_type = result["predictions"][0]["tagName"]
        confidence = result["predictions"][0]["probability"]

        # Actualizar el modelo ImageData con los resultados del análisis
        image_data.detected_tree_type = predicted_tree_type
        image_data.confidence = confidence
        image_data.analysis_date = timezone.now()  # Asegúrate de importar timezone desde django.utils
        image_data.save()
    else:
        # Manejar errores según sea necesario
        print(f"Error en la solicitud a la API de Custom Vision: {response.status_code}")
from django.core.files.storage import FileSystemStorage

from django.conf import settings
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

from azure.storage.blob import BlobServiceClient, ContentSettings
from django.http import HttpResponse
from django.shortcuts import render

# ... Configurar conexión a Azure Blob Storage ...

def cargar_imagen(request):
    if request.method == 'POST':
        # Obtener la imagen del formulario
        image = request.FILES['image']

        # Guardar la imagen en el contenedor de Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=droniastorage1;AccountKey=jEeBo8Rs7WYR9IBtqefg13jedRAGYDPJtDLdc86ek+kz1jJ0dJUtW7FaGgOuCN1JAD1RiApAChYV+AStlUrakQ==;EndpointSuffix=core.windows.net")
        container_name = "imagenes-sin-procesar"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=image.name)
        blob_client.upload_blob(image, content_settings=ContentSettings(content_type='image/jpeg'))

        return HttpResponse("Imagen cargada exitosamente en Azure Blob Storage")

    return render(request, 'carga.html')  # Renderizar un formulario HTML para cargar la imagen

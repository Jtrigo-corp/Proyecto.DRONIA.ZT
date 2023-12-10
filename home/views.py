from azure.storage.blob import BlobServiceClient, ContentSettings
from map.models import Imagenes, Vuelo
from map.forms import DatosForm, IngresarVueloForm
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
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
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import folium
from dotenv import load_dotenv
from map.models import Vuelo
from rest_framework import views, response
from api.serializers import *
import os
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib import messages

def ingresar_vuelo(request):
    if request.method == 'POST':
        form = IngresarVueloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cargar_imagen')  # Puedes redirigir a donde desees después de ingresar el vuelo
    else:
        form = IngresarVueloForm()

    vuelos = Vuelo.objects.all()
    return render(request, 'cargar_imagen.html', {'form': form, 'vuelos': vuelos})

def index(request):

    context = {
        'segment': 'index',
        # 'products' : Product.objects.all()
    }
    return render(request, "pages/index.html", context)


def ubicacion(request):
    ubicaciones = Ubicacion.objects.all()
    initialMap = folium.Map(location=[-27.370371, -70.322529], zoom_start=13.5)
    context = {
        'segment': 'ubicacion',
        'home': initialMap._repr_html_(),
        # 'products' : Product.objects.all()
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

def list_muestreo(request):
    muestreo = list(Muestreo.objects.values())
    data = {'muestreo': muestreo}
    return JsonResponse(data)

def delete_muestreo(request, id):
    muestreo = get_object_or_404(Muestreo, id=id)

    if request.method == 'POST':
        muestreo.delete()
        return redirect('cargar_imagen')

    return render(request, 'cargar_imagen.html', {'muestreo': muestreo})
# ... Configurar conexión a Azure Blob Storage ...

def edit_muestreo(request, id):
    muestreo = get_object_or_404(Muestreo, id=id)

    if request.method == 'POST':
        form = DatosForm(request.POST, instance=muestreo)
        if form.is_valid():
            form.save()
            return redirect('cargar_imagen')
    else:
        form = DatosForm(instance=muestreo)

    return render(request, 'edit_muestreo.html', {'form': form, 'muestreo': muestreo}) 

def cargar_imagen(request):
    if request.method == 'POST':
        form_vuelo = IngresarVueloForm(request.POST)
        if form_vuelo.is_valid():
            form_vuelo.save()

        formulario = DatosForm(vuelos=Vuelo.objects.all(), data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()

            # Obtener el vuelo asociado al formulario
            vuelo = formulario.cleaned_data['vuelo']

            # Resto del código para guardar imágenes
            images = request.FILES.getlist('image')
            blob_service_client = BlobServiceClient.from_connection_string("Tu conexión a Azure Storage")

            for image in images:
                # Verificar si la imagen ya existe en Azure Blob Storage
                blob_client = blob_service_client.get_blob_client(container="imagenes-sin-procesar", blob=image.name)

                if blob_client.exists():
                    messages.warning(request, 'La imagen ya existe en Azure Blob Storage.')
                else:
                    # Subir la imagen a Azure Blob Storage
                    blob_client.upload_blob(image, content_settings=ContentSettings(content_type='image/jpeg'))

                    # Guardar la información de la imagen en la base de datos
                    Imagenes.objects.create(vuelo=vuelo, nombre_imagen=image.name)

            return redirect('cargar_imagen')
    else:
        form_vuelo = IngresarVueloForm()
        formulario = DatosForm(vuelos=Vuelo.objects.all())

    informaciones = Vuelo.objects.all()
    return render(request, 'cargar_imagen.html', {'form_vuelo': form_vuelo, 'formulario': formulario, 'informaciones': informaciones})

load_dotenv()

def resultados(request):
    
    key = os.getenv('KEY')
    endpoint = os.getenv('ENDPOINT')
    project_id = os.getenv('PROJECT_ID')
    published_name = os.getenv('PUBLISHED_ITERATION_NAME')
    credentials = ApiKeyCredentials(in_headers={'Prediction-key': key})
    client = CustomVisionPredictionClient(endpoint, credentials)

    # cliente de Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
    container_client = blob_service_client.get_container_client(os.getenv('CONTAINER_NAME1'))

    # Obtener las últimas 2 imágenes del contenedor
    blobs_list = container_client.list_blobs()
    latest_blobs = sorted(blobs_list, key=lambda blob: blob.last_modified, reverse=True)[:2]

    container_client_analizadas = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING')).get_container_client('imagenes-analizadas')

    # Clasificar cada imagen, guardar los resultados y la imagen analizada
    results = []
    for i, blob in enumerate(latest_blobs):
        blob_client = blob_service_client.get_blob_client(os.getenv('CONTAINER_NAME1'), blob.name)
        blob_data = blob_client.download_blob().readall()
        result = client.classify_image(project_id, published_name, blob_data)
        for prediction in result.predictions:
            results.append({
                'id': i + 1,
                'fecha': blob.last_modified,
                'tag_name': prediction.tag_name,
                'probability': prediction.probability
            })
            print(f'{prediction.tag_name}: {(prediction.probability):.2%}')
        # Guardar la imagen analizada en el contenedor 'imagenes-analizadas'
        
        container_client_analizadas.upload_blob(f'imagen_{result.id}.jpg', blob_data, overwrite=True)

    # Renderizar la plantilla con los resultados
    return render(request, 'resultados.html', {'results': results})

def edit_vuelo(request, id):
    vuelo = get_object_or_404(Vuelo, id=id)
    if request.method == 'POST':
        form = DatosForm(request.POST, instance=vuelo)
        if form.is_valid():
            form.save()
            return redirect('cargar_imagen')
    else:
        form = DatosForm(instance=vuelo)
    return render(request, 'edit_vuelo.html', {'form': form})

def delete_vuelo(request, id_vuelo):
    vuelo = get_object_or_404(Vuelo, id_vuelo=id_vuelo)

    if request.method == 'POST':
        vuelo.delete()
        return HttpResponseRedirect('/cargar_imagen/')  # Cambiar a la URL correcta

    return render(request, 'cargar_imagen.html', {'vuelos': vuelo})
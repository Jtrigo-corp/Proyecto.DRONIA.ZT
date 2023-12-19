from gettext import translation
import imghdr
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings
import requests
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
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from azure.storage.blob import BlobServiceClient, ContentSettings
from django.shortcuts import render, redirect
from django.contrib import messages
from map.forms import IngresarVueloForm, DatosForm
from map.models import Vuelo, Imagenes
from django.contrib import messages
import mimetypes
import os
from azure.storage.blob import BlobServiceClient
from django.http import JsonResponse
# Asegúrate de tener esta línea al inicio de tu archivo
from django.db import transaction


def ingresar_vuelo(request):
    if request.method == 'POST':
        form = IngresarVueloForm(request.POST)
        if form.is_valid():
            form.save()
            # Puedes redirigir a donde desees después de ingresar el vuelo
            return redirect('cargar_imagen')
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


def show_map(request):
    # Crear un mapa de Folium
    m = folium.Map(location=[-27.370371, -70.322529], zoom_start=13.5)

    # Convertir el mapa a HTML
    m = m._repr_html_()

    # Pasar el mapa a la plantilla
    context = {'my_map': m}
    return render(request, 'ubicaciones.html', context)


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


def contar_blobs(contenedor):
    connection_string = "DefaultEndpointsProtocol=https;AccountName=droniastorage1;AccountKey=+5rxQ1nhKb/I+d7JnFZ91nRRebO7YRnwHLu2pJ5KOIyMXRUsI91Q8iQfJY/VOkhRuZziAu/vhnVr+AStdjSyHw==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string)
    container_client = blob_service_client.get_container_client(contenedor)
    blobs_list = container_client.list_blobs()
    return len(list(blobs_list))


# Uso de la función
cantidad_predicciones = contar_blobs("imagenes-analizadas")


def cargar_imagen(request):
    if request.method == 'POST':
        form_vuelo = IngresarVueloForm(request.POST)
        if form_vuelo.is_valid():
            form_vuelo.save()

        formulario = DatosForm(vuelos=Vuelo.objects.all(),
                               data=request.POST, files=request.FILES)
        print(request.FILES)  # Imprime los archivos subidos
        if formulario.is_valid():
            with transaction.atomic():
                # Guardar el formulario en la base de datos
                formulario.save()

                # Obtener el vuelo asociado al formulario
                vuelo = formulario.cleaned_data['vuelo']

                load_dotenv('.env')
                # Resto del código para guardar imágenes en Azure Blob Storage
                try:
                    # Verificar que el código se está ejecutando
                    print("Iniciando la subida de imágenes...")
                    images = request.FILES.getlist('image')
                    # Verificar que estás obteniendo las imágenes correctamente
                    print(f"Imágenes: {images}")

                    os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=https;AccountName=droniastorage1;AccountKey=ajoSCjr7SO3Ix2jUmAXjOpOkM5wo6fwLicXRk9qYKdYryUjOnmwobl7Fmyus0titUygcsqVCWPHb+AStWXW6Bw==;EndpointSuffix=core.windows.net'

                    blob_service_client = BlobServiceClient.from_connection_string(
                        os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

                    for image in images:
                        blob_client = blob_service_client.get_blob_client(
                            container="imagenes-sin-procesar", blob=image.name)
                        # Verificar que estás creando el BlobClient correctamente
                        print(f"BlobClient: {blob_client}")

                        if blob_client.exists():
                            messages.warning(
                                request, 'La imagen ya existe en Azure Blob Storage.')
                        else:
                            content_type, _ = mimetypes.guess_type(image.name)
                            if content_type is None:
                                content_type = 'application/octet-stream'

                            # Verificar que el código se está ejecutando
                            print("Subiendo imagen...")
                            blob_client.upload_blob(
                                image, content_settings=ContentSettings(content_type=content_type))
                            Imagenes.objects.create(
                                vuelo=vuelo, nombre_imagen=image.name, analizada=True)
                except Exception as e:
                    print(f"Error al cargar imágenes: {e}")
                    messages.error(
                        request, 'Ocurrió un error al cargar las imágenes.')
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")

                return redirect('cargar_imagen')
        else:
            print(formulario.errors)  # Imprime los errores del formulario
            # Verificar si el formulario es válido
            print("El formulario no es válido.")
    else:
        form_vuelo = IngresarVueloForm()
        formulario = DatosForm(vuelos=Vuelo.objects.all())

    informaciones = Vuelo.objects.all()
    return render(request, 'cargar_imagen.html', {'form_vuelo': form_vuelo, 'formulario': formulario, 'informaciones': informaciones})


def resultados(request):
    # Obtener todos los vuelos y la información relacionada
    vuelos = Vuelo.objects.all()
    vuelos_info = []
    for vuelo in vuelos:
        imagenes = Imagenes.objects.filter(vuelo=vuelo, analizada=True)
        results = predict_images(imagenes)
        vuelos_info.append({
            'vuelo': vuelo.id_vuelo,
            'cantidad_imagenes': imagenes.count(),
            'fecha': vuelo.fecha_vuelo,  # Solo la fecha, sin la hora
            'resultados': results,  # Los resultados de la predicción
        })

    # Renderizar la plantilla con la información de los vuelos
    return render(request, 'resultados.html', {'vuelos_info': vuelos_info})

def detalle_vuelo(request, id_vuelo):
    vuelo = Vuelo.objects.get(id=id_vuelo)
    data = {
        'fecha_carga': vuelo.fecha_carga,
        'operador': vuelo.operador.username,
        'cantidad_imagenes': vuelo.cantidad_imagenes,
        'cantidad_predicciones': vuelo.cantidad_predicciones,
    }
    return JsonResponse(data)


def predecir_imagenes(request, id_vuelo):
    # Obtener las imágenes del contenedor
    images = Imagenes.objects.filter(vuelo_id=id_vuelo)

    # Predecir las imágenes usando Custom Vision
    results = predict_images(images)

    # Devolver los resultados como una respuesta JSON
    return JsonResponse({'results': results})


def predict_images(images):
    # Configuración para Custom Vision
    ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
    prediction_key = "d34506be224747ad9e403b138e1977d1"
    project_id = "6f464655-adf2-46f4-a04a-979ee9c7ed63"
    publish_iteration_name = "Modelo-Train"

    # Crear un cliente de predicción
    credentials = ApiKeyCredentials(
        in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

    # Crear un cliente de Azure Blob Storage
    os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=https;AccountName=droniastorage1;AccountKey=ajoSCjr7SO3Ix2jUmAXjOpOkM5wo6fwLicXRk9qYKdYryUjOnmwobl7Fmyus0titUygcsqVCWPHb+AStWXW6Bw==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

    # Imprimir los nombres de todos los blobs en el contenedor 'imagenes-sin-procesar'
    container_client = blob_service_client.get_container_client('imagenes-sin-procesar')
    blobs = container_client.list_blobs()

    for blob in blobs:
        print(blob.name)

    # Predecir cada imagen
    results = []
    print("Iniciando la predicción de las imágenes...")  # Nueva declaración de impresión
    for image in images:
        blob_client = blob_service_client.get_blob_client(
            container="imagenes-sin-procesar", blob=image.nombre_imagen)

        if blob_client.exists():
            stream = blob_client.download_blob().readall()
            result = predictor.classify_image(project_id, publish_iteration_name, stream)
            # Obtén el tag con el mayor porcentaje
            top_prediction = max(result.predictions, key=lambda prediction: prediction.probability)
            # Convierte el porcentaje a un formato de porcentaje
            percentage = round(top_prediction.probability * 100, 1)
            # Almacena el nombre del tag y el porcentaje
            results.append((image.nombre_imagen, top_prediction.tag_name, f"{percentage}%"))
        else:
            print(f"La imagen con ID {image.id_imagen} no existe en el blob storage.")
    return results


def validar_imagenes(request, id_vuelo):
    # Configuración para Custom Vision
    ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
    prediction_key = "d34506be224747ad9e403b138e1977d1"
    project_id = "6f464655-adf2-46f4-a04a-979ee9c7ed63"
    publish_iteration_name = "Modelo-Train"

    # Crear un cliente de predicción
    credentials = ApiKeyCredentials(
        in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

    # Crear un cliente de Azure Blob Storage
    os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=https;AccountName=droniastorage1;AccountKey=ajoSCjr7SO3Ix2jUmAXjOpOkM5wo6fwLicXRk9qYKdYryUjOnmwobl7Fmyus0titUygcsqVCWPHb+AStWXW6Bw==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

    # Obtener una lista de todos los blobs en el contenedor 'imagenes-sin-procesar'
    container_client = blob_service_client.get_container_client('imagenes-sin-procesar')
    blobs = container_client.list_blobs()

    # Predecir cada imagen
    results = []
    for blob in blobs:
        # Verificar si el nombre del blob comienza con el ID del vuelo
        if blob.name.startswith(str(id_vuelo)):
            blob_client = blob_service_client.get_blob_client(
                container="imagenes-sin-procesar", blob=blob.name)

            if blob_client.exists():
                stream = blob_client.download_blob().readall()
                result = predictor.classify_image(project_id, publish_iteration_name, stream)
                # Obtén el tag con el mayor porcentaje
                top_prediction = max(result.predictions, key=lambda prediction: prediction.probability)
                # Convierte el porcentaje a un formato de porcentaje
                percentage = round(top_prediction.probability * 100, 1)
                # Almacena el nombre del tag y el porcentaje
                results.append((blob.name, top_prediction.tag_name, f"{percentage}%"))
            else:
                print(f"El blob con nombre {blob.name} no existe en el blob storage.")
    return results


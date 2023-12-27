from gettext import translation
import imghdr
from io import BytesIO
from urllib import request
from azure.storage.blob import BlobServiceClient, ContentSettings
import requests
from datetime import datetime, timedelta
from map.models import AreaMuestreo, Imagenes, Vuelo
from map.forms import AreaMuestreoForm, DatosForm, IngresarVueloForm
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
from azure.core.exceptions import AzureError
from azure.cognitiveservices.vision.customvision.prediction.models import CustomVisionErrorException
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

    # Obtener todas las áreas de muestreo
    areasMuestreo = AreaMuestreo.objects.all()

    # Agregar un marcador para cada área de muestreo
    for area in areasMuestreo:
        if area.latitud is not None and area.longitud is not None:  # Asegúrate de que la latitud y la longitud no sean None
            popup = folium.Popup(f'Descripcion: {area.direccion}', max_width=500)  # Aumenta el ancho máximo del popup
            folium.Marker(
                location=[area.latitud, area.longitud],
                popup=popup,
            ).add_to(m)

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
        
        form_vuelo = IngresarVueloForm()  # Define form_vuelo aquí
        formulario = DatosForm()  # Define formulario aquí
        if request.method == 'POST':
            form_area = AreaMuestreoForm(request.POST)
            form_vuelo = IngresarVueloForm(request.POST)
            formulario = DatosForm(request.POST, request.FILES)  # Asigna un valor a formulario
            if form_vuelo.is_valid():
                form_vuelo.save()
                return redirect('cargar_imagen')

            if form_area.is_valid():
                form_area.save()
                return redirect('cargar_imagen')

            print(request.FILES)  # Imprime los archivos subidos
            if formulario.is_valid():
                with transaction.atomic():
                    # Guardar el formulario en la base de datos
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
                            Imagenes.objects.create(vuelo=vuelo, nombre_imagen=image.name, analizada=False)
                            
                    messages.success(request, '¡Las imagenes se subieron satisfactoriamente!')
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
        form_area = AreaMuestreoForm()
        form_vuelo = IngresarVueloForm()
        formulario = DatosForm(vuelos=Vuelo.objects.all())

    informaciones = Vuelo.objects.all()
    return render(request, 'cargar_imagen.html', {'form_vuelo': form_vuelo, 'formulario': formulario, 'informaciones': informaciones, 'form_area': form_area})

import json
from django.core.serializers import serialize
from django.shortcuts import render

def some_view(request):
    vuelos = Vuelo.objects.all()  # Obtén todos los objetos Vuelo
    vuelos_json = serializers.serialize('json', vuelos)
    return render(request, 'ubicaciones.html', {'vuelos': vuelos_json})

def resultados(request):
    # Obtener todos los vuelos y la información relacionada
    vuelos = Vuelo.objects.all()
    vuelos_info = []
    for vuelo in vuelos:
        # Obtén solo las imágenes que han sido analizadas y tienen un resultado
        imagenes = Imagenes.objects.filter(vuelo=vuelo, analizada=True, resultado__isnull=False)
        imagenes_sin_analizar = Imagenes.objects.filter(vuelo=vuelo, analizada=False)
        imagenes_nuevas = Imagenes.objects.filter(vuelo=vuelo, analizada=False).count()  # Contador de imágenes nuevas

        vuelos_info.append({
            'vuelo': vuelo.id_vuelo,
            'cantidad_imagenes': imagenes.count(),
            'cantidad_imagenes_nuevas': imagenes_nuevas,  # Agregar la cantidad de imágenes nuevas al contexto
            'fecha': vuelo.fecha_vuelo,
            'resultados': [(imagen.nombre_imagen, imagen.resultado, imagen.porcentaje_prediccion) for imagen in imagenes],
        })

    # Renderizar la plantilla con la información de los vuelos
    return render(request, 'resultados.html', {'vuelos_info': vuelos_info})



def predecir_imagenes(request, id_vuelo):
    # Obtener las imágenes del contenedor
    images = Imagenes.objects.filter(vuelo_id=id_vuelo)

    # Predecir las imágenes usando Custom Vision
    results, errors = predict_images(images, id_vuelo)
    for error in errors:
        messages.error(request, error)

    # Devolver los resultados como una respuesta JSON
    return JsonResponse({'results': results})


def predict_images(images, id_vuelo):
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

    # Obtener el vuelo y las imágenes nuevas
    vuelo = Vuelo.objects.get(id_vuelo=id_vuelo)
    images = Imagenes.objects.filter(vuelo=vuelo, analizada=False)  

    # Crear clientes de contenedor para 'imagenes-analizadas' e 'imagenes-sin-procesar'
    sin_procesar_container_client = blob_service_client.get_container_client('imagenes-sin-procesar')
    analizadas_container_client = blob_service_client.get_container_client('imagenes-analizadas')


    # Predecir cada imagen
    errors = []
    results = []
    print("Iniciando la predicción de las imágenes...")
    for image in images:
        blob_client = None
        if image.nombre_imagen:
            blob_client = sin_procesar_container_client.get_blob_client(image.nombre_imagen)


        if blob_client and blob_client.exists():
            imagenes = Imagenes.objects.filter(nombre_imagen=image.nombre_imagen)
            for imagen in imagenes:
                if imagen.resultado is None:
                    streamdownloader = blob_client.download_blob().readall()
                    # Comprobar el tamaño de la imagen
                    if len(streamdownloader) > 4 * 1024 * 1024:  # 4 MB
                        errors.append(f"Error: La imagen {image.nombre_imagen} es demasiado grande para ser clasificada por Custom Vision.")
                    else:
                        # Realizar la predicción
                        try:
                            prediction = predictor.classify_image(project_id, publish_iteration_name, streamdownloader)
                            top_prediction = max(prediction.predictions, key=lambda prediction: prediction.probability)
                            percentage = round(top_prediction.probability * 100, 1)
                            # Almacena el nombre del tag y el porcentaje
                            results.append((blob.name, top_prediction.tag_name, f"{percentage}%"))

                            # Actualizar la imagen con el resultado de la predicción
                            imagen.resultado = top_prediction.tag_name
                            imagen.porcentaje_prediccion = percentage
                            imagen.analizada = True
                            imagen.save()

                            try:
                                # Mover la imagen al contenedor 'imagenes-analizadas'
                                analizadas_blob_client = analizadas_container_client.get_blob_client(imagen.nombre_imagen)
                                analizadas_blob_client.upload_blob(streamdownloader, overwrite=True)
                                blob_client.delete_blob()
                            except CustomVisionErrorException as e:
                                if 'format' in str(e):  # Comprobar si el error se debe al formato de la imagen
                                    errors.append(f"Error: El formato de la imagen {image.nombre_imagen} es incorrecto.")
                                else:
                                    errors.append(f"Error: La imagen {image.nombre_imagen} está corrupta o no cumple con los requisitos de predicción de Custom Vision.")
                                continue
                            results.append({
                                'nombre_imagen': imagen.nombre_imagen,
                                'resultado': imagen.resultado,
                                'porcentaje_prediccion': imagen.porcentaje_prediccion
                            })
                        except CustomVisionErrorException as e:
                            messages.error(request, f"Error: La imagen {image.nombre_imagen} está corrupta o no cumple con los requisitos de predicción de Custom Vision.")    
                        #messages.success(request, 'Las imágenes se analizaron satisfactoriamente por la inteligencia artificial.')
            
        else:
            print(f"La imagen con nombre {image.nombre_imagen} ya existe en el blob storage.")
            
    return results, errors



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


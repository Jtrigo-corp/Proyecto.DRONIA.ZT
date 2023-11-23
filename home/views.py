from http import HTTPStatus
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.core.files.storage import FileSystemStorage
import boto3
import json
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import folium
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

class ValidateView(views.APIView):
    def post(self, request, *args, **kwargs):
        s3 = boto3.client('s3')
        runtime = boto3.client('runtime.sagemaker')

        file = request.FILES['photo']
        file_name = default_storage.save(file.name, file)
        s3.upload_file(file_name, 'dronia-bucket-imagenes', file.name)

        with open(file_name, 'rb') as file_obj:
            result = runtime.invoke_endpoint(
                EndpointName='YourSageMakerEndpoint',
                Body=file_obj.read(),
                ContentType='application/x-image'
            )

        prediction = json.loads(result['Body'].read().decode())
        return response.Response(f"El árbol frutal reconocido es {prediction['fruitTreeType']} con un porcentaje de aprobación de {prediction['approvalPercentage']}%")

class UploadView(views.APIView):
    def post(self, request):
        uploaded_file = request.FILES['photo']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        file_name = fs.url(name)

        s3 = boto3.client('s3')
        s3.upload_file(file_name, 'dronia-bucket-imagenes', uploaded_file.name)

        rekognition = boto3.client('rekognition')
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'dronia-bucket-imagenes',
                    'Name': uploaded_file.name
                }
            },
            MaxLabels=10
        )

        runtime = boto3.client('runtime.sagemaker')
        with open(file_name, 'rb') as file_obj:
            result = runtime.invoke_endpoint(
                EndpointName='YourSageMakerEndpoint',
                Body=file_obj.read(),
                ContentType='application/x-image'
            )

        prediction = json.loads(result['Body'].read().decode())
        return render(request, 'carga.html', {'prediction': prediction})      
from django.core.files.storage import FileSystemStorage
import boto3
import json
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import folium
from rest_framework import views, response


# Create your views here.
def analisis(request):
  context = {
    'segment': 'analisis'
  }
  return render(request, "pages/analisis.html", context)

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
      

def upload(request):
    if request.method == 'POST':
        image_file = request.FILES['image_file']

        # Guardar el archivo de imagen temporalmente
        image_file_name = default_storage.save(image_file.name, image_file)

        # Crear un cliente S3
        s3 = boto3.client('s3')

        # Subir el archivo de imagen al bucket S3
        s3.upload_file(image_file_name, 'dronia-bucket-imagenes', image_file.name)

        return JsonResponse({'message': 'Imagen subida correctamente a S3.'})

    return JsonResponse({'message': 'Método no permitido.'}, status=405)
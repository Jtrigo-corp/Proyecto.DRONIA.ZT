import boto3
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import folium
from rest_framework import views, response

from django.core.files.storage import default_storage

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
        s3.upload_file(file_name, 'mybucket', file.name)

        with open(file_name, 'rb') as file_obj:
            result = runtime.invoke_endpoint(
                EndpointName='YourSageMakerEndpoint',
                Body=file_obj.read(),
                ContentType='application/x-image'
            )

        return response.Response(result['Body'].read().decode())
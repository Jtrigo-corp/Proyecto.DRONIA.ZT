from http import HTTPStatus
from django.http import Http404, JsonResponse
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


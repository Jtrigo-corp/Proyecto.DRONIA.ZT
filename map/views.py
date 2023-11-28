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


# Create your views here.
def analisis(request):
    context = {
        'segment': 'analisis'
    }
    return render(request, "pages/analisis.html", context)


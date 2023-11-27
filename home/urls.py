from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('tables/', views.tables, name='tables'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('mapanalisis/', views.mapanalisis, name='mapanalisis'),
    path('list_vuelos/', views.list_vuelos, name='list_vuelos'),
    path('carga/', views.carga, name='carga'),
    path('upload/', views.upload_image, name='upload_image'),
    path('analyze/', views.analyze_image, name='analyze_image'),
    path('analyze-images/', views.analyze_images, name='analyze_images'),
]

from django.urls import path
from map.views import UploadView
from map.views import cargar_imagen
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),
  path('tables/', views.tables, name='tables'),
  path('ubicacion/', views.ubicacion, name='ubicacion'),
  path('mapanalisis/', views.mapanalisis, name='mapanalisis'),
  path('list_vuelos/', views.list_vuelos, name='list_vuelos'),
  path('carga/', views.carga, name='carga'),
  path('upload/', UploadView.as_view(), name='upload'),
  path('cargar_imagen/', cargar_imagen, name='cargar_imagen'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('tables/', views.tables, name='tables'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('resultados/', views.resultados, name='resultados'),
    path('list_vuelos/', views.list_vuelos, name='list_vuelos'),
    path('carga/', views.carga, name='carga'),
    path('cargar_imagen/', views.cargar_imagen, name='cargar_imagen'),
    path('ingresar_vuelo/', views.ingresar_vuelo, name='ingresar_vuelo'),
    path('detalle_vuelo/<int:id_vuelo>/',
         views.detalle_vuelo, name='detalle_vuelo'),
    path('predecir_imagenes/<int:id_vuelo>/',
         views.predecir_imagenes, name='predecir_imagenes'),


]

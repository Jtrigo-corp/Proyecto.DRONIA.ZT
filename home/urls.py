from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index,  name='index'),
    path('tables/', views.tables, name='tables'),
    #path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('resultados/', views.resultados, name='resultados'),
    path('list_vuelos/', views.list_vuelos, name='list_vuelos'),
    path('carga/', views.carga, name='carga'),
    path('cargar_imagen/', views.cargar_imagen, name='cargar_imagen'),
    path('ingresar_vuelo/', views.ingresar_vuelo, name='ingresar_vuelo'),
    #path('detalle_vuelo/<int:id_vuelo>/',
     #    views.detalle_vuelo, name='detalle_vuelo'),
    path('validar_imagenes/<int:id_vuelo>/',
         views.validar_imagenes, name='validar_imagenes'),
    path('ubicaciones/', views.show_map, name='ubicaciones'),
    path('mapa/', views.show_map, name='show_map'),
    path('predict_images/<int:id_vuelo>/', views.predict_images, name='predict_images'),
    #path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('resultados/predecir_imagenes/<int:id_vuelo>/', views.predecir_imagenes, name='predecir_imagenes'),



]

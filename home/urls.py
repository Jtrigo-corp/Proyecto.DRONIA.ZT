from django.urls import path
from home.views import UploadView
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

]

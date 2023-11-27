from typing import Any
from django.db import models

# Create your models here.
class Vuelo(models.Model):
    id = models.AutoField(primary_key=True)
    norte = models.FloatField()
    este = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vuelo'

class Ubicacion(models.Model):
    id_vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    id_ubicacion = models.AutoField(primary_key=True, verbose_name='ID Ubicacion')
    latitud = models.FloatField(verbose_name='Latitud')
    longitud = models.FloatField(verbose_name='Longitud')
    poblacion_ubicada = models.CharField(max_length=250, verbose_name='Poblacion Ubicada')
    
    class Meta:
        db_table = 'ubicacion'
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['id_ubicacion']
        
    def __str__(self):
        return self.name
        
class ImageData(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    flight_number = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    analysis_date = models.DateTimeField(null=True, blank=True)
    detected_tree_type = models.CharField(max_length=50, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
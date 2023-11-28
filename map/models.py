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
        
# models.py
class Muestreo(models.Model):
    nro_vuelo = models.CharField(max_length=50)
    latitud = models.FloatField()
    longitud = models.FloatField()
    direccion = models.CharField(max_length=255)
    fecha_muestreo = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'muestreo'
    
    def __str__(self):
        return f'{self.nro_vuelo} - {self.fecha_muestreo}'
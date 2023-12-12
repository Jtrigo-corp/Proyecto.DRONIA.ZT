
from time import timezone
from django.db import models

class Operador(models.Model):
    id_operador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    mail = models.EmailField()
    class Meta:
        db_table = 'map_operador'
        
    def __str__(self):
        return f'Operador {self.id_operador} - {self.nombre} {self.apellido}'

class Vuelo(models.Model):
    id_vuelo = models.AutoField(primary_key=True)
    sector_vuelo = models.CharField(max_length=255)
    fecha_vuelo = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE,blank=True, null=True)
    cantidad_imagenes = models.IntegerField(default=0)
    cantidad_predicciones = models.IntegerField(default=0)
    class Meta:
        db_table = 'map_vuelo'  # Especifica el nombre de la tabla en la base de datos

    def __str__(self):
        return f'Vuelo {self.id_vuelo}'

class Imagenes(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    vuelo = models.ForeignKey('Vuelo', on_delete=models.CASCADE)
    nombre_imagen = models.CharField(max_length=255, blank=True, null=True)
    resultado = models.TextField(null=True, blank=True)
    image_file = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    analizada = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'map_imagenes'  # Especifica el nombre de la tabla en la base de datos
    
class Ubicaciones(models.Model):
    id_ubicaciones = models.AutoField(primary_key=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    numero_asignacion = models.IntegerField()
    class Meta:
        db_table = 'map_ubicaciones'

    def __str__(self):
        return f'Ubicacion {self.id_ubicaciones}'

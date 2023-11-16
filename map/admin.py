from django.contrib import admin
from .models import Vuelo, Ubicacion

# Register your models here.
admin.site.register(Vuelo)
admin.site.register(Ubicacion)
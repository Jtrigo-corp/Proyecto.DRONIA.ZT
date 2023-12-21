import multiprocessing
import os
import sys

from core.settings import BASE_DIR

bind = "0.0.0.0:8000"  # Puedes ajustar el puerto según tus necesidades
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = "gunicorn_error.log/"  # Reemplaza con la ruta correcta
loglevel = "info"
sys.path.append(os.path.join(BASE_DIR, "src"))
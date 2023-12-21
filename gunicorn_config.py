import multiprocessing

bind = "0.0.0.0:8000"  # Puedes ajustar el puerto según tus necesidades
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = "gunicorn_error.log/"  # Reemplaza con la ruta correcta
loglevel = "info"

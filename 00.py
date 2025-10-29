import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.workflow.tasks import execute_overpass

if __name__ == "__main__":
    # disparar tarea de prueba
    result = execute_overpass.delay(123)
    print("Task queued:", result)
    # opcional: esperar resultado si tenés result backend configurado
    try:
        print("Result ready?:", result.ready())
        print("Result get (with timeout 10s):", result.get(timeout=10))
    except Exception as e:
        print("No se pudo obtener resultado desde result backend:", e)

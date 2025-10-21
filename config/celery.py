import os
from celery import Celery

# Config Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

#  settings de Django con el namespace CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# descubre tareas de forma automática
app.autodiscover_tasks()

#  debug para ver que las tasks se registran
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

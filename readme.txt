
habilitar redis mediante docker, usar pws o directamente desde docker

cerciorate de que pgadmin4 tenga la base corriendo de forma correcta

python manage.py runserver

celery: 

celery -A config worker --loglevel=info -P solo -Q selenium_jobs
celery -A config worker --loglevel=info -P solo -Q overpass_queries

http://127.0.0.1:8000/api/accounts/register/

http://127.0.0.1:8000/api/accounts/login/

http://127.0.0.1:8000/api/workflows/

http://127.0.0.1:8000/api/workflows/<id_del_workflow>/

http://127.0.0.1:8000/api/workflows/<id_del_workflow>/export/

http://127.0.0.1:8000/api/workflows/<id_del_workflow>/download/
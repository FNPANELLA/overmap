después de ejecutar pip install -r requirements.txt, ejecutar:
python -m spacy download es_core_news_sm

VARIABLES DE ENTORNO

WEBDRIVER_PATH  = directorio de chromedriver
DEBUG_STATE = True o False
PASSWORD = contraseña de tu base de datos (postgres)
SECRET_KEY =  es el resultado de:
import secrets
secrets.token_hex(32) 


habilitar redis mediante docker, usar pws o directamente desde docker

cerciorate de que pgadmin4 tenga la base corriendo de forma correcta

python manage.py runserver

celery; se pueden usar dos terminales dentro del venv o una sola si se fusiona mediante el codigo las listas de trabajo o mediante el query de celery

celery -A config worker --loglevel=info -P solo -Q selenium_jobs,overpass_queries

celery -A config worker --loglevel=info -P solo -Q selenium_jobs
celery -A config worker --loglevel=info -P solo -Q overpass_queries

http://127.0.0.1:8000/api/accounts/register/

http://127.0.0.1:8000/api/accounts/login/

http://127.0.0.1:8000/api/workflows/

http://127.0.0.1:8000/api/workflows/<id_del_workflow>/

http://127.0.0.1:8000/api/workflows/<id_del_workflow>/export/

http://127.0.0.1:8000/api/workflows/<id_del_workflow>/download/

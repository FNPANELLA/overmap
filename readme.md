# Overmap

Overmap es una aplicación web y API que transforma consultas en lenguaje natural en conjuntos de datos.

El sistema traduce la consulta usando NLP, obtiene datos de OpenStreetMap, enriquece los resultados con Selenium (buscando email, redes sociales, etc.) y exporta un CSV. El proceso se gestiona mediante tareas asíncronas con Celery.

## Stack

Django, Django Rest Framework, Celery, Redis, PostgreSQL, SpaCy, Selenium, Pandas, GeoPy.

## Instalación y Configuración

### 1\. Prerrequisitos

Python 3.x
PostgreSQL
Redis
Un WebDriver (ej. `chromedriver`)

### 2\. Clonar e Instalar Dependencias

git clone [https://github.com/tu-usuario/overmap.git](https://www.google.com/search?q=https://github.com/tu-usuario/overmap.git)
cd overmap

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m spacy download es\_core\_news\_sm

### 3\. Configuración del Entorno

Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

SECRET\_KEY=tu\_secret\_key\_de\_django
DEBUG\_STATE=True
PASSWORD=tu\_contraseña\_de\_postgres\_db
WEBDRIVER\_PATH=/usr/local/bin/chromedriver

### 4\. Base de Datos

Cerciorate de haber creado una base de datos en PostgreSQL llamada `overmap_db`.

Aplica las migraciones de Django:

python manage.py migrate

## Cómo Ejecutar la Aplicación

Necesitas 2 o 3 terminales abiertas en la raíz del proyecto.

### Terminal 1: Servidor de Django

python manage.py runserver

### Terminal 2: Workers de Celery

celery -A config worker --loglevel=info -P solo -Q selenium\_jobs,overpass\_queries

## API Endpoints

POST /api/accounts/register/
POST /api/accounts/login/
GET, POST /api/workflows/
GET /api/workflows/[int:pk](https://www.google.com/search?q=int:pk)/
POST /api/workflows/[int:pk](https://www.google.com/search?q=int:pk)/export/
GET /api/workflows/[int:pk](https://www.google.com/search?q=int:pk)/download/
GET /api/results/[int:pk](https://www.google.com/search?q=int:pk)/

hecho en 1 semana con amor por Federico Panella
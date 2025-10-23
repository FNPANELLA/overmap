#config de bd django y etc

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG_STATE") #dev

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#
#SESSION_ENGINE = 'django.contrib.sessions.backends.file'
#SESSION_FILE_PATH = os.path.join(BASE_DIR, 'django_sessions')
#SESSION_SAVE_EVERY_REQUEST = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'apps.accounts',
    'apps.workflow',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'], # directorio global de plantillas 
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'overmap_db',
        'USER': 'postgres',
        'PASSWORD': os.environ.get("PASSWORD"),
        'HOST': 'localhost',
        'PORT': '5432',
    }


}
AUTH_PASSWORD_VALIDATORS = [
    
]
# internacionalizacion
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"
# asegurar de que tu servidor redis este corriendo 
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ROUTES = {
    'apps.workflow.tasks.execute_overpass': {'queue': 'overpass_queries'},
    'apps.workflow.tasks.run_selenium_job': {'queue': 'selenium_jobs'},
}
SPACY_MODEL = 'es_core_news_sm'
SELENIUM_WEBDRIVER_PATH = os.environ.get('WEBDRIVER_PATH')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

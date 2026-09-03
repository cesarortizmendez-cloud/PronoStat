"""
PronoStat — Configuración principal de Django.
Laboratorio educativo de Análisis de Datos, Series de Tiempo y Pronósticos.
Dr. César Ortiz Méndez · Ingeniería Industrial · USACH

Misma arquitectura que IO-Lab Pro: cada módulo es una app independiente,
cálculo stateless (JSON entra / JSON sale), sin modelos custom, estáticos con WhiteNoise.
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-pronostat-dev-key-cambiar-en-produccion')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
CSRF_TRUSTED_ORIGINS = [
    o for o in config('CSRF_TRUSTED_ORIGINS', default='https://*.vercel.app').split(',') if o
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    # Módulos de PronoStat (cada uno es una app independiente)
    'apps.home',
    'apps.datos',
    'apps.descriptiva',
    'apps.regresion',
    'apps.pronostico',
    'apps.exportar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'pronostat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': ['django.template.context_processors.request']},
    },
]

WSGI_APPLICATION = 'pronostat.wsgi.application'

# No se usan modelos custom: el cálculo es stateless. SQLite queda solo por compatibilidad.
DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}
}

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# CompressedStaticFilesStorage (sin manifest) evita tener que correr collectstatic
# para el desarrollo local con runserver, y sigue sirviendo comprimido en Vercel.
STORAGES = {
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Payloads de datos pueden ser grandes (datasets); ampliamos el límite.
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024  # 25 MB

"""
Configuración de Django para el proyecto Ecommerce.

Este archivo contiene todas las configuraciones del proyecto Django, incluyendo:
- Configuración de base de datos
- Configuración de aplicaciones instaladas
- Configuración de middleware
- Configuración de archivos estáticos y multimedia
- Configuración de CORS para permitir peticiones desde el frontend
- Configuración de seguridad

Generado por 'django-admin startproject' usando Django 5.2.8.

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.2/topics/settings/

Para la lista completa de configuraciones y sus valores, ver:
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

# Importar Path de pathlib para manejo de rutas multiplataforma
from pathlib import Path
# Importar config de python-decouple para leer variables de entorno
# Permite leer configuraciones desde archivo .env sin exponer secretos en el código
from decouple import config

# Construir rutas dentro del proyecto así: BASE_DIR / 'subdir'.
# BASE_DIR es la ruta absoluta del directorio raíz del proyecto
# Se usa para construir rutas relativas a archivos y directorios del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================================
# CONFIGURACIONES DE SEGURIDAD
# ============================================================================
# Configuraciones rápidas de desarrollo - no adecuadas para producción
# Ver https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡mantener la clave secreta usada en producción en secreto!
# SECRET_KEY se usa para firmar cookies, sesiones, tokens CSRF, etc.
# En producción, debe estar en variables de entorno y nunca en el código
# Se lee desde variable de entorno SECRET_KEY o usa un valor por defecto (solo desarrollo)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-!6-_+el9_oulfxq1pw8r8&ey!d3jk&*c$$_6)8^5r6n62n%vwx')

# ADVERTENCIA DE SEGURIDAD: ¡no ejecutar con debug activado en producción!
# DEBUG=True muestra información detallada de errores (útil en desarrollo)
# DEBUG=False en producción para ocultar información sensible
# Se lee desde variable de entorno DEBUG o usa False por defecto
DEBUG = config('DEBUG', default='False') == 'True'

# ALLOWED_HOSTS para producción (Render)
# Lista de dominios/hosts permitidos que pueden servir esta aplicación Django
# Previene ataques de Host Header Injection
# Se lee desde variable de entorno ALLOWED_HOSTS o usa valores por defecto
# En producción, debe contener solo el dominio real del servidor
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1,192.168.2.5,192.168.0.15'
).split(',')  # Convertir string separado por comas a lista


# ============================================================================
# DEFINICIÓN DE APLICACIONES INSTALADAS
# ============================================================================
# Lista de todas las aplicaciones Django instaladas en el proyecto
# Django ejecutará las migraciones y buscará modelos/templates en estas apps

INSTALLED_APPS = [
    # Aplicaciones contribuidas por Django (incluidas por defecto)
    'django.contrib.admin',  # Panel de administración de Django
    'django.contrib.auth',  # Sistema de autenticación de Django
    'django.contrib.contenttypes',  # Framework de tipos de contenido
    'django.contrib.sessions',  # Framework de sesiones
    'django.contrib.messages',  # Framework de mensajes
    'django.contrib.staticfiles',  # Manejo de archivos estáticos (CSS, JS, imágenes)
    
    # Aplicaciones de terceros
    'corsheaders',  # Para permitir CORS (Cross-Origin Resource Sharing) desde cualquier frontend
                    # Necesario para que el frontend React pueda hacer peticiones al backend
    
    # Aplicaciones propias del proyecto
    'totalisting',  # App para gestión de productos, categorías y licencias
    'useraccount',  # App para autenticación y registro de usuarios
]

# ============================================================================
# MIDDLEWARE
# ============================================================================
# Lista de middleware que se ejecuta en cada petición HTTP
# El orden es importante: se ejecutan de arriba hacia abajo en requests,
# y de abajo hacia arriba en responses

MIDDLEWARE = [
    # SecurityMiddleware: Agrega headers de seguridad HTTP
    'django.middleware.security.SecurityMiddleware',
    
    # CorsMiddleware: Maneja CORS headers (debe estar antes de otros middlewares)
    # Permite que el frontend React haga peticiones al backend
    'corsheaders.middleware.CorsMiddleware',
    
    # WhiteNoiseMiddleware: Sirve archivos estáticos en producción (Render)
    # Más eficiente que servir archivos estáticos con Django en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    # SessionMiddleware: Maneja sesiones de usuario
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # CommonMiddleware: Agrega funcionalidades comunes (normalización de URLs, etc.)
    'django.middleware.common.CommonMiddleware',
    
    # CsrfViewMiddleware: Protección CSRF (Cross-Site Request Forgery)
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # AuthenticationMiddleware: Asocia usuarios con requests usando sesiones
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # MessageMiddleware: Maneja mensajes temporales para el usuario
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # XFrameOptionsMiddleware: Previene clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================================
# CONFIGURACIÓN DE URLS Y TEMPLATES
# ============================================================================
# ROOT_URLCONF: Módulo Python que contiene las URLs principales del proyecto
# Django buscará el archivo urls.py en este módulo
ROOT_URLCONF = 'Ecommerce.urls'

# TEMPLATES: Configuración del sistema de plantillas de Django
# Aunque este proyecto usa API REST (no templates), Django requiere esta configuración
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de templates Django
        'DIRS': [],  # Directorios adicionales para buscar templates (vacío = solo en apps)
        'APP_DIRS': True,  # Buscar templates en subdirectorio 'templates' de cada app
        'OPTIONS': {
            'context_processors': [
                # Procesadores de contexto que agregan variables a todos los templates
                'django.template.context_processors.request',  # Agrega el objeto request
                'django.contrib.auth.context_processors.auth',  # Agrega información del usuario
                'django.contrib.messages.context_processors.messages',  # Agrega mensajes
            ],
        },
    },
]

# WSGI_APPLICATION: Ruta al objeto WSGI callable usado por el servidor WSGI
# WSGI (Web Server Gateway Interface) es el estándar para servir aplicaciones Python web
WSGI_APPLICATION = 'Ecommerce.wsgi.application'


# ============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Importar sys para detectar si estamos ejecutando tests
import sys

# Configuración de base de datos para tests (usa SQLite en memoria)
# Cuando se ejecutan tests, Django usa una base de datos en memoria para mayor velocidad
# ':memory:' crea una base de datos SQLite temporal en RAM que se elimina al terminar
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Motor de base de datos SQLite
            'NAME': ':memory:',  # Base de datos en memoria (solo para tests)
        }
    }
else:
    # Configuración de base de datos SQLite3 para desarrollo y producción
    # SQLite es una base de datos ligera basada en archivos, perfecta para proyectos pequeños
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Motor de base de datos SQLite
            'NAME': BASE_DIR / 'db.sqlite3',  # Ruta al archivo de base de datos SQLite
            # El archivo db.sqlite3 se crea automáticamente en el directorio raíz del proyecto
        }
    }


# ============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
# Lista de validadores que se aplican cuando se crean/actualizan contraseñas
# Estos validadores mejoran la seguridad de las contraseñas de usuarios

AUTH_PASSWORD_VALIDATORS = [
    # Valida que la contraseña no sea muy similar a información del usuario
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Valida que la contraseña tenga una longitud mínima (por defecto 8 caracteres)
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # Valida que la contraseña no esté en una lista de contraseñas comunes
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    # Valida que la contraseña no sea completamente numérica
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================================================
# INTERNACIONALIZACIÓN (i18n)
# ============================================================================
# https://docs.djangoproject.com/en/5.2/topics/i18n/
# Configuración para soporte de múltiples idiomas y zonas horarias

# Código de idioma por defecto (español de España)
LANGUAGE_CODE = 'es-es'

# Zona horaria por defecto (UTC - Coordinated Universal Time)
TIME_ZONE = 'UTC'

# Habilitar internacionalización (traducción de textos)
USE_I18N = True

# Usar zonas horarias (aware datetime objects)
USE_TZ = True


# ============================================================================
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# ============================================================================
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# URL base para servir archivos estáticos (CSS, JavaScript, imágenes)
# En desarrollo, Django sirve estos archivos automáticamente
# En producción, se deben servir con un servidor web o WhiteNoise
STATIC_URL = '/static/'

# Directorio donde Django recopilará todos los archivos estáticos para producción
# Se ejecuta con: python manage.py collectstatic
# Convertir a string para compatibilidad con algunas versiones de Django
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

# Configuración de archivos multimedia (imágenes subidas por usuarios)
# MEDIA_URL: URL base para acceder a archivos multimedia
# Ejemplo: /media/categories/star-wars.jpg
MEDIA_URL = '/media/'

# MEDIA_ROOT: Directorio del sistema de archivos donde se guardan los archivos multimedia
# Ejemplo: /path/to/project/media/
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de WhiteNoise para servir archivos estáticos en producción
# WhiteNoise permite servir archivos estáticos directamente desde Django sin necesidad
# de un servidor web separado (útil para despliegues en Render, Heroku, etc.)
# CompressedStaticFilesStorage comprime los archivos para reducir el tamaño
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# ============================================================================
# CONFIGURACIÓN DE MODELOS
# ============================================================================
# Tipo de campo de clave primaria por defecto para modelos Django
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
# BigAutoField es un IntegerField de 64 bits (soporta hasta 9,223,372,036,854,775,807)
# Se usa automáticamente si no se especifica primary_key en un modelo
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# CONFIGURACIÓN DE CORS (Cross-Origin Resource Sharing)
# ============================================================================
# CORS permite que el frontend React (que corre en un puerto diferente)
# pueda hacer peticiones HTTP al backend Django sin ser bloqueado por el navegador
# Configurado para permitir acceso desde cualquier frontend (proyecto educativo)

# Permitir CORS desde cualquier origen (solo para proyectos educativos)
# En producción, esto debería ser False y usar CORS_ALLOWED_ORIGINS con dominios específicos
CORS_ALLOW_ALL_ORIGINS = True

# Métodos HTTP permitidos en las peticiones CORS
# Estos son los métodos que el frontend puede usar para comunicarse con el backend
CORS_ALLOW_METHODS = [
    'DELETE',  # Eliminar recursos
    'GET',     # Obtener recursos
    'OPTIONS', # Preflight requests (verificación previa)
    'PATCH',   # Actualización parcial de recursos
    'POST',    # Crear recursos o enviar datos
    'PUT',     # Actualizar recursos completos
]

# Headers HTTP permitidos en las peticiones CORS
# Estos headers pueden ser enviados por el frontend en las peticiones
CORS_ALLOW_HEADERS = [
    'accept',           # Tipos de contenido aceptados
    'accept-encoding',  # Codificación aceptada (gzip, etc.)
    'authorization',    # Token de autenticación
    'content-type',     # Tipo de contenido enviado (application/json, etc.)
    'dnt',              # Do Not Track header
    'origin',           # Origen de la petición
    'user-agent',       # Información del navegador/cliente
    'x-csrftoken',      # Token CSRF para protección
    'x-requested-with', # Indica que es una petición AJAX
]

# Permitir credenciales (cookies, headers de autenticación) en peticiones CORS
# Esto permite que el frontend envíe cookies y headers de autenticación
CORS_ALLOW_CREDENTIALS = True

# ⚠️ NOTA DE SEGURIDAD:
# CORS_ALLOW_ALL_ORIGINS = True permite acceso desde cualquier dominio.
# Esto es adecuado para proyectos educativos y desarrollo, pero NO para producción.
# En producción, deberías usar:
#   CORS_ALLOW_ALL_ORIGINS = False
#   CORS_ALLOWED_ORIGINS = ['https://tudominio.com', 'https://www.tudominio.com']
# Esto restringe el acceso solo a dominios específicos y confiables.

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-locadora-secret-key-change-in-production-xyz123"
)

DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'gestao.apps.GestaoConfig',
    'pwa',
]

PWA_APP_NAME = "LocaGestão"

PWA_APP_DESCRIPTION = "Sistema de Gestão para Locadora"

PWA_APP_THEME_COLOR = "#0d6efd"

PWA_APP_BACKGROUND_COLOR = "#ffffff"

PWA_APP_DISPLAY = "standalone"

PWA_APP_SCOPE = "/"

PWA_APP_ORIENTATION = "portrait"

PWA_APP_START_URL = "/"

PWA_APP_STATUS_BAR_COLOR = "default"

PWA_APP_ICONS = [
    {
        "src": "/static/icons/icon-192.png",
        "sizes": "192x192"
    },
    {
        "src": "/static/icons/icon-512.png",
        "sizes": "512x512"
    }
]

PWA_APP_SPLASH_SCREEN = [
    {
        "src": "/static/icons/icon-512.png",
        "media": "(device-width: 768px)"
    }
]

PWA_APP_DIR = "ltr"

PWA_APP_LANG = "pt-BR"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = 'gestao.Usuario'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

CORS_ALLOW_ALL_ORIGINS = True

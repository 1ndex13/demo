"""Настройки проекта «Учусь РФ»."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

#Основные настройки проекта
SECRET_KEY = 'Shamsutdinov-Ainur-19.05.2026'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'courses.apps.CoursesConfig',
    'panel.apps.PanelConfig',
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

ROOT_URLCONF = 'uchurf.urls'

#Шаблоны
TEMPLATES = [
    {
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
    },
]

WSGI_APPLICATION = 'uchurf.wsgi.application'

#База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#Валидация
AUTH_USER_MODEL = 'accounts.User'
AUTH_PASSWORD_VALIDATORS = []

#Язык системы
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

#Формат дат
DATE_INPUT_FORMATS = ['%d.%m.%Y', '%Y-%m-%d']
DATE_FORMAT = 'd.m.Y'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

#Откуда будут брать картинки
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Перенаправления на шаблоны
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/cabinet/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

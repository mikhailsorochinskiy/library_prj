from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
import dj_database_url

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

ALLOWED_HOSTS = ['library-prj.onrender.com', '127.0.0.1', '144.31.89.239']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
    'library',
    'django_filters',
    'corsheaders',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Render даёт одну строку DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
    print("✅ Using PostgreSQL from DATABASE_URL")
else:
    # Локальная разработка
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT'),
        }
    }
    print("⚠️ Using local PostgreSQL - check DATABASE_URL on Render!")

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
# Для продакшена на Render
if not DEBUG:
    # Папка, где будут собираться статичные файлы
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Включи WhiteNoise для обработки статики
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

else:
    # Для разработки
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Настройки для загрузки файлов
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 МБ в памяти
FILE_UPLOAD_PERMISSIONS = 0o644  # права доступа к файлам
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50 МБ для всего запроса

# Разрешенные типы файлов (для безопасности)
SECURE_CONTENT_TYPE_NOSNIFF = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Вариант A: Разреши всё (для разработки)
CORS_ALLOW_ALL_ORIGINS = True  # ← поставь True пока

# Вариант B: Разреши только определённые домены (для продакшена)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # React dev server
#     "http://localhost:8080",  # Vue dev server
#     "https://ваш-фронтенд.сайт",  # твой фронтенд
# ]

# Разреши отправку cookies (если нужна аутентификация)
CORS_ALLOW_CREDENTIALS = True

# Разрешенные методы
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Разрешенные заголовки
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# На время разработки письма будут падать в консоль терминала
if os.getenv('EMAIL_HOST_USER'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@library.com'
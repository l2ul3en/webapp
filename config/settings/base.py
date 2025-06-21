from pathlib import Path
from os import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# Application definition

BASE_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'incidents',
    'cobertura',
    'bitacora',
    'reports',
]

THIRD_APPS = [
    'django_tables2',
    'crispy_forms',
    'crispy_bootstrap5',
    'import_export',
]

INSTALLED_APPS = BASE_INSTALLED_APPS + LOCAL_APPS + THIRD_APPS

BASE_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOCAL_MIDDLEWARE = [

]

THIRD_MIDDLEWARE = [

]

MIDDLEWARE = BASE_MIDDLEWARE + LOCAL_MIDDLEWARE + THIRD_MIDDLEWARE

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#table boostrap5 django-tables2
DJANGO_TABLES2_TEMPLATE="django_tables2/bootstrap5-responsive.html"
DJANGO_TABLES2_TABLE_ATTRS = {
    'class': 'table table-light table-hover table-sm align-middle',
    'tbody': {
        'class': 'table-group-divider',
    }
}

#URL redirect
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
    
#https://stackoverflow.com/questions/31670231/autologout-a-user-after-specific-time-in-django
SESSION_COOKIE_AGE = 30 * 60  # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session whenever user is active

#Vars crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

#Vars Zabbix Reports
try:
    ZABBIX_URL = environ["ZABBIX_URL"]
    ZABBIX_TOKEN = environ["ZABBIX_TOKEN"]
except KeyError as e:
    raise KeyError(f"Environment variable {e} is not set. Please set it in your environment variables.") from e
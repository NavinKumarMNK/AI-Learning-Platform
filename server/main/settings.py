import os
import datetime
import logging

from pathlib import Path
from utils import base
from django.core.files.storage import FileSystemStorage

from meglib.ml.api import Llm, Embedding
from meglib.ml.store import VectorDB
from meglib.ml.preprocessor import DocumentProcessor
from meglib.ml.loaders import PDFLoader

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEGACAD_DIR = os.path.join(BASE_DIR, "megacad")

# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
CONFIG = base.load_config(BASE_DIR / "config.yaml")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DJANGO_DEBUG", False)
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cassandra_engine",
    "megacad",
    "api.v1.chat",
    "api.v1.user",
    "api.v1.course",
    "rest_framework",
    # "rest_framework.authtoken",
    # "rest_framework_simplejwt",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # "meglib.middleware.errors.Log500ErrorsMiddleware"
]

# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#        "rest_framework.authentication.SessionAuthentication",
#        "rest_framework.authentication.TokenAuthentication",
#        "rest_framework_simplejwt.authentication.JWTAuthentication",
#    ],
#    "DEFAULT_PERMISSION_CLASSES": [
#        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
#    ],
# }

# CORS_URLS_REGEX = r"^api/.*"
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = ["http://localhost:1234"]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "static/megacad/"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"
ASGI_APPLICATION = "main.asgi.app"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
    },
    "cassandra": {
        "ENGINE": "django_cassandra_engine",
        "NAME": os.environ.get("CASSANDRA_KEYSPACE"),
        "HOST": os.environ.get("CASSANDRA_HOST"),
        "USER": os.environ.get("CASSANDRA_USER"),
        "PASSWORD": os.environ.get("CASSANDRA_PASSWORD"),
        "OPTIONS": {
            "replication": {"strategy_class": "SimpleStrategy", "replication_factor": 2}
        },
    },
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/megacad/static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TempFileSystemStorage = FileSystemStorage(location="/tmp")

STORAGES = {
    "temp_storage": {
        "BACKEND": TempFileSystemStorage,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Logger
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
}


LLM_API = Llm(
    host=os.environ.get("ML_SERVICE_HOST"),
    port=os.environ.get("ML_SERVICE_PORT"),
    endpoint=os.environ.get("LLM_ENDPOINT"),
)

EMBED_API = Embedding(
    host=os.environ.get("ML_SERVICE_HOST"),
    port=os.environ.get("ML_SERVICE_PORT"),
    endpoint=os.environ.get("EMBEDDING_ENDPOINT"),
)

QDRANT_CONFIG = CONFIG["store"]
LLM_CONFIG = CONFIG["llm"]
QDRANT_DB = VectorDB(QDRANT_CONFIG["config"])
DOC_PROC_CONFIG = CONFIG["doc_processor"]
DOC_PROCESSOR = DocumentProcessor()
PDF_LOADER = PDFLoader()

"""
Django settings for pescasr project (production-ready minimal adjustments).
Hecho para usar en Railway con MySQL (mysql-connector) y servir static con Whitenoise.
"""

import os
from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers
from urllib.parse import urlparse, unquote

# Cargar variables de entorno desde .env (solo en desarrollo)
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Security / env
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", os.environ.get("DJANGO_DEBUG", "false")).lower() in ("1", "true", "yes")

# aceptar hosts de entorno o incluir testserver para los tests
_raw_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

# Apps (mantengo tus apps + necesarios)
INSTALLED_APPS = [
    "ventas",
    "users",
    "productos",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # terceros
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "users.middleware.UserRegisterLoggingMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pescasr.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "pescasr.wsgi.application"

# Helper: parse a mysql URL like mysql://user:pass@host:port/dbname
def _db_from_url(url: str):
    parsed = urlparse(url)
    name = parsed.path.lstrip("/") if parsed.path else ""
    user = unquote(parsed.username) if parsed.username else ""
    password = unquote(parsed.password) if parsed.password else ""
    host = parsed.hostname or ""
    port = str(parsed.port) if parsed.port else "3306"
    return {
        "default": {
            "ENGINE": "mysql.connector.django",
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }

# DATABASE: soporta MYSQL_URL/DATABASE_URL (connection string) o variables individuales; si no, fallback a SQLite (dev)
mysql_url = os.environ.get("MYSQL_URL") or os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_PUBLIC_URL")
if mysql_url:
    DATABASES = _db_from_url(mysql_url)
elif os.environ.get("MYSQL_HOST") and os.environ.get("MYSQL_DATABASE") and os.environ.get("MYSQL_USER"):
    DATABASES = {
        "default": {
            "ENGINE": "mysql.connector.django",
            "NAME": os.environ.get("MYSQL_DATABASE"),
            "USER": os.environ.get("MYSQL_USER"),
            "PASSWORD": os.environ.get("MYSQL_PASSWORD", ""),
            "HOST": os.environ.get("MYSQL_HOST"),
            "PORT": os.environ.get("MYSQL_PORT", "3306"),
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# Static + Whitenoise
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF / JWT / Schema
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ.get("JWT_ACCESS_MINUTES", "30"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ.get("JWT_REFRESH_DAYS", "7"))),
    "ROTATE_REFRESH_TOKENS": False,
    "AUTH_HEADER_TYPES": tuple(os.environ.get("JWT_AUTH_HEADER_TYPES", "Bearer").split(",")),
}

# Custom user model (si lo tenés)
AUTH_USER_MODEL = "users.User"

# CORS / CSRF (ajustar desde env en Railway)
# Prefer FRONTEND_URL if provided, otherwise fall back to CORS_ALLOWED_ORIGINS env
_frontend = os.environ.get("FRONTEND_URL")
if _frontend:
    CORS_ALLOWED_ORIGINS = [_frontend]
else:
    CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Allow all origins in DEBUG to ease local development
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# Control credentials via env (JWT in headers normally doesn't need credentials)
CORS_ALLOW_CREDENTIALS = os.environ.get("CORS_ALLOW_CREDENTIALS", "false").lower() in ("1", "true", "yes")

# Ensure Authorization header is allowed (case-insensitive)
CORS_ALLOW_HEADERS = list(default_headers) + ["authorization", "Authorization"]

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://localhost:3000").split(",")

SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")
CSRF_COOKIE_SAMESITE = os.environ.get("CSRF_COOKIE_SAMESITE", "Lax")
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False").lower() in ("1", "true", "yes")
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "False").lower() in ("1", "true", "yes")

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "users": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": os.environ.get("SPECTACULAR_TITLE", "Pescasr API"),
    "DESCRIPTION": "Documentación de la API",
    "VERSION": os.environ.get("SPECTACULAR_VERSION", "1.0.0"),
}
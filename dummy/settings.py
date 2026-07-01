import os
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url

# --------------------------------------------------
# Base Directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# Security
# --------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this")

DEBUG = os.getenv("DEBUG", "False").lower() in (
    "1",
    "true",
    "yes",
    "on",
)

# --------------------------------------------------
# Allowed Hosts
# --------------------------------------------------

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

extra_hosts = os.getenv("ALLOWED_HOSTS")

if extra_hosts:
    for host in extra_hosts.split(","):
        host = host.strip()
        if host:
            ALLOWED_HOSTS.append(host)

# Remove duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

# --------------------------------------------------
# Installed Apps
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "WeatherForcast",
]

# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# HTTPS Settings (Production Only)
# --------------------------------------------------

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --------------------------------------------------
# CSRF Trusted Origins
# --------------------------------------------------

CSRF_TRUSTED_ORIGINS = []

if render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")

extra_hosts = os.getenv("ALLOWED_HOSTS")

if extra_hosts:
    for host in extra_hosts.split(","):
        host = host.strip()
        if host and host not in ("localhost", "127.0.0.1"):
            CSRF_TRUSTED_ORIGINS.append(f"https://{host}")

# --------------------------------------------------
# URLs
# --------------------------------------------------

ROOT_URLCONF = "dummy.urls"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# --------------------------------------------------
# Templates
# --------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dummy.wsgi.application"

# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# --------------------------------------------------
# Password Validators
# --------------------------------------------------

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

# --------------------------------------------------
# Internationalization
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# --------------------------------------------------
# User Model
# --------------------------------------------------

AUTH_USER_MODEL = "WeatherForcast.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------
# Email Settings
# --------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"

EMAIL_TIMEOUT = 20

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --------------------------------------------------
# API Keys
# --------------------------------------------------

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# --------------------------------------------------
# Static Files
# --------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
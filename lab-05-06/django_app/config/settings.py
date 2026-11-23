"""Налаштування локального навчального проєкту Django."""

import os
from pathlib import Path
from secrets import token_urlsafe


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or token_urlsafe(48)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]"]

INSTALLED_APPS = [
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_app.workshops.apps.WorkshopsConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "django_app.config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
CSRF_FAILURE_VIEW = "django_app.workshops.views.csrf_rejected"
CSRF_COOKIE_HTTPONLY = True

LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = [PROJECT_ROOT / "shared" / "static"]

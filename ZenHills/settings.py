import os   
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SECURITY ────────────────────────────────────────────────────────────────

SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-change-in-production")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "yeshraj.pythonanywhere.com",
    "zenhillsjourneys.com",
    "www.zenhillsjourneys.com",
]

# ─── APPS ────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "accounts",
    "enquiries",
]

AUTH_USER_MODEL = "accounts.User"

# ─── MIDDLEWARE ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ZenHills.urls"

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

WSGI_APPLICATION = "ZenHills.wsgi.application"

# ─── DATABASE ─────────────────────────────────────────────────────────────────
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# ─── AUTH PASSWORD VALIDATORS ────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── TIME ────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"  
USE_I18N = True
USE_TZ = True

# ─── STATIC FILES ────────────────────────────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── CORS ────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "https://zenhills-journeys.vercel.app",
    "https://zenhillsjourneys.com",
    "https://www.zenhillsjourneys.com",
]
# CORS_ALLOW_ALL_ORIGINS = True 

#! ─── EMAIL if switched to pythonanywhere pro
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "zenhills53@gmail.com")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")  
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#! ─── EMAIL if switched to pythonanywhere pro

SENDGRID_API_KEY  = os.environ.get("SENDGRID_API_KEY", "")
ZENHILLS_FROM_EMAIL = "zenhills53@gmail.com"
ZENHILLS_FROM_NAME  = "ZenHills Journeys"
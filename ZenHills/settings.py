import os   
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SECURITY ────────────────────────────────────────────────────────────────
# Store these in PythonAnywhere's environment variables, NEVER in this file.
# PythonAnywhere: Web tab → "Environment variables" section

SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-change-in-production")

# Reads from env — set DEBUG=False in PythonAnywhere env vars
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "yeshraj.pythonanywhere.com",
    "localhost",
    "127.0.0.1",
    #! Add your custom domain here if you get one
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
# Uses DATABASE_URL env var if set (Railway/Postgres), else falls back to SQLite
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

# ─── INTERNATIONALISATION ────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"   # changed from UTC — you're in IST
USE_I18N = True
USE_TZ = True

# ─── STATIC FILES ────────────────────────────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── CORS ────────────────────────────────────────────────────────────────────
# Only allow your actual frontend origins — not everything
CORS_ALLOWED_ORIGINS = [
    "https://zenhills-journeys.vercel.app",
    "http://localhost:8080",
    "http://localhost:5173",   # Vite dev server
]
# CORS_ALLOW_ALL_ORIGINS = True  # ← never use this in production

# ─── EMAIL ───────────────────────────────────────────────────────────────────
# Store EMAIL_HOST_PASSWORD as an environment variable in PythonAnywhere.
# NEVER hardcode credentials in this file.
# Steps:
#   1. Go to Google Account → Security → App Passwords
#   2. Revoke the old password (it's exposed on GitHub)
#   3. Generate a new app password
#   4. In PythonAnywhere Web tab → add env var: EMAIL_HOST_PASSWORD = <new password>

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "zenhills53@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")  # set in env, never here
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
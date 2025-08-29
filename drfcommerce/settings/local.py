from .base import *

# Local development settings

DEBUG = True

# SQLite database for local testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Allow local hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Easier email backend for dev (prints emails to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

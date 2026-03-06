# auth password hashing requires SECRET_KEY even in tests
SECRET_KEY = "test-insecure-key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    # contenttypes + auth are here so migrations create auth_user table,
    # needed by admin view tests (tests/admin/) for superuser creation
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django_edne_cep",
    "django_edne_cep.cep_tables",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# lookup_cep service uses caching, locmem avoids external dependencies
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django_edne_cep",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from django.apps import AppConfig


class DjangoEdneCepConfig(AppConfig):
    name = "django_edne_cep"
    verbose_name = "Django eDNE CEP"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import checks  # noqa: F401, PLC0415

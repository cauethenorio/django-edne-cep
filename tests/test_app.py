from django.apps import apps


def test_app_is_installed():
    assert apps.is_installed("django_edne_cep")


def test_app_config():
    config = apps.get_app_config("django_edne_cep")
    assert config.verbose_name == "Django eDNE CEP"

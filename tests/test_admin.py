from django.contrib import admin
from django.test import override_settings

from django_edne_cep.models import Cep


@override_settings(
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django_edne_cep",
        "django_edne_cep.cep_tables",
    ],
    EDNE_CEP={"ADMIN_ENABLED": True},
)
def test_admin_registers_cep_when_enabled():
    from django_edne_cep.admin import register_admin  # noqa: PLC0415

    site = admin.AdminSite()
    register_admin(site)

    assert Cep in site._registry


@override_settings(
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django_edne_cep",
        "django_edne_cep.cep_tables",
    ],
    EDNE_CEP={"ADMIN_ENABLED": True},
)
def test_admin_registers_cep_tables_models():
    from django_edne_cep.cep_tables.admin import (  # noqa: PLC0415
        register_cep_tables_admin,
    )
    from django_edne_cep.cep_tables.models import (  # noqa: PLC0415
        Bairro,
        Localidade,
        Logradouro,
    )

    site = admin.AdminSite()
    register_cep_tables_admin(site)

    assert Localidade in site._registry
    assert Bairro in site._registry
    assert Logradouro in site._registry


@override_settings(
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django_edne_cep",
        "django_edne_cep.cep_tables",
    ],
)
def test_cep_tables_admin_does_not_register_when_disabled():
    from django_edne_cep.cep_tables.admin import (  # noqa: PLC0415
        register_cep_tables_admin,
    )
    from django_edne_cep.cep_tables.models import Localidade  # noqa: PLC0415

    site = admin.AdminSite()
    register_cep_tables_admin(site)

    assert Localidade not in site._registry


@override_settings(
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django_edne_cep",
    ],
)
def test_admin_does_not_register_when_disabled():
    from django_edne_cep.admin import register_admin  # noqa: PLC0415

    site = admin.AdminSite()
    register_admin(site)

    assert Cep not in site._registry


@override_settings(
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.admin",
        "django_edne_cep",
    ],
    EDNE_CEP={"ADMIN_ENABLED": True},
)
def test_admin_registers_only_cep_without_cep_tables():
    from django_edne_cep.admin import register_admin  # noqa: PLC0415

    site = admin.AdminSite()
    register_admin(site)

    assert Cep in site._registry
    # cep_tables models should not be registered since the app is not installed
    assert len(site._registry) == 1


def test_cep_admin_is_read_only():
    from django_edne_cep.admin import CepAdmin  # noqa: PLC0415

    assert CepAdmin.has_add_permission(None, None) is False
    assert CepAdmin.has_change_permission(None, None) is False
    assert CepAdmin.has_delete_permission(None, None) is False


def test_cep_admin_has_search_and_filters():
    from django_edne_cep.admin import CepAdmin  # noqa: PLC0415

    assert "cep" in CepAdmin.search_fields
    assert "municipio" in CepAdmin.search_fields
    assert "uf" in CepAdmin.list_filter

from django.apps import apps
from django.core.checks import Warning as CheckWarning
from django.core.checks import register
from django.db import connections
from edne_correios_loader import TableSetEnum

from .settings import get_setting
from .table_names import get_table_name


@register()
def check_tables_exist(app_configs, **kwargs):  # noqa: ARG001
    alias = get_setting("DATABASE_ALIAS")
    connection = connections[alias]
    existing_tables = connection.introspection.table_names()

    # always check cep_unificado
    expected = ["cep_unificado"]

    # add tables based on the configured table_set
    table_set = _get_expected_table_set()
    if table_set is not None:
        expected = table_set.to_populate()

    missing = [
        get_table_name(name)
        for name in expected
        if get_table_name(name) not in existing_tables
    ]

    if not missing:
        return []

    tables_str = ", ".join(missing)
    return [
        CheckWarning(
            f"Missing tables: {tables_str}. "
            "Run 'manage.py load_edne_cep' to populate CEP data.",
            id="django_edne_cep.W001",
        )
    ]


def _get_expected_table_set():
    """Determine which table set is expected based on settings and installed apps"""
    explicit = get_setting("TABLE_SET")
    if explicit is not None:
        return TableSetEnum(explicit)

    if apps.is_installed("django_edne_cep.cep_tables"):
        return TableSetEnum.CEP_TABLES

    return None

from django.core.checks import Warning as CheckWarning
from django.core.checks import register
from django.db import connections

from .settings import get_setting
from .table_names import get_table_name


@register()
def check_tables_exist(app_configs, **kwargs):  # noqa: ARG001
    warnings = []
    alias = get_setting("DATABASE_ALIAS")
    connection = connections[alias]

    table_name = get_table_name("cep_unificado")
    existing_tables = connection.introspection.table_names()

    if table_name not in existing_tables:
        warnings.append(
            CheckWarning(
                f"Table '{table_name}' does not exist. "
                "Run 'manage.py load_dne' to populate CEP data.",
                id="django_edne_cep.W001",
            )
        )

    return warnings

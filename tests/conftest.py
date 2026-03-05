import pytest
from django.db import connection


@pytest.fixture(scope="session")
def _create_unmanaged_tables(django_db_setup, django_db_blocker):  # noqa: ARG001
    """Create tables for unmanaged models so tests can query them."""
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cep_unificado (
                    cep VARCHAR(8) PRIMARY KEY,
                    logradouro VARCHAR(100),
                    complemento VARCHAR(100),
                    bairro VARCHAR(72),
                    municipio VARCHAR(72) NOT NULL,
                    municipio_cod_ibge INTEGER NOT NULL,
                    uf VARCHAR(2) NOT NULL,
                    nome VARCHAR(100)
                )
                """
            )

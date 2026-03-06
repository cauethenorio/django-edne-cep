import pytest
from django.db import connection

CREATE_CEP_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS edne_cep (
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


@pytest.fixture(scope="session")
def _cep_table(django_db_setup, django_db_blocker):  # noqa: ARG001
    """Create the edne_cep table for tests that query the Cep model directly."""
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CEP_TABLE_SQL)

import pytest
from django.test import override_settings

from django_edne_cep.checks import check_tables_exist


def _mock_table_names(mocker, tables):
    """Mock connection introspection to return given table list."""
    mock_conn = mocker.MagicMock()
    mock_conn.introspection.table_names.return_value = tables
    mocker.patch("django_edne_cep.checks.connections", {"default": mock_conn})


@pytest.mark.django_db
def test_check_warns_when_tables_missing(mocker):
    _mock_table_names(mocker, [])

    warnings = check_tables_exist(app_configs=None, databases=None)
    assert len(warnings) == 1
    assert warnings[0].id == "django_edne_cep.W001"
    assert "edne_cep" in warnings[0].msg


@pytest.mark.django_db
def test_check_includes_cep_tables_when_installed(mocker):
    """cep_tables is in INSTALLED_APPS (test settings)"""
    _mock_table_names(mocker, [])

    warnings = check_tables_exist(app_configs=None, databases=None)
    assert "edne_localidade" in warnings[0].msg


@override_settings(EDNE_CEP={"TABLE_SET": "all"})
@pytest.mark.django_db
def test_check_includes_all_tables_when_configured(mocker):
    _mock_table_names(mocker, [])

    warnings = check_tables_exist(app_configs=None, databases=None)
    assert "log_faixa_uf" in warnings[0].msg


@pytest.mark.django_db
def test_check_passes_when_tables_exist(mocker):
    _mock_table_names(
        mocker,
        [
            "edne_cep",
            "edne_localidade",
            "edne_bairro",
            "edne_logradouro",
            "edne_caixa_postal",
            "edne_grande_usuario",
            "edne_unidade_operacional",
        ],
    )

    warnings = check_tables_exist(app_configs=None, databases=None)
    assert len(warnings) == 0

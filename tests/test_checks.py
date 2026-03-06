import pytest
from django.test import override_settings

from django_edne_cep.checks import check_tables_exist


@pytest.mark.django_db
def test_check_warns_when_tables_missing():
    warnings = check_tables_exist(app_configs=None, databases=None)
    assert len(warnings) == 1
    assert warnings[0].id == "django_edne_cep.W001"
    assert "edne_cep" in warnings[0].msg


@pytest.mark.django_db
def test_check_includes_cep_tables_when_installed():
    """cep_tables is in INSTALLED_APPS (test settings)"""
    warnings = check_tables_exist(app_configs=None, databases=None)
    assert "edne_localidade" in warnings[0].msg


@override_settings(EDNE_CEP={"TABLE_SET": "all"})
@pytest.mark.django_db
def test_check_includes_all_tables_when_configured():
    warnings = check_tables_exist(app_configs=None, databases=None)
    assert "log_faixa_uf" in warnings[0].msg

import pytest

from django_edne_cep.checks import check_tables_exist


@pytest.mark.django_db
def test_check_warns_when_cep_table_missing():
    warnings = check_tables_exist(app_configs=None)
    assert len(warnings) >= 1
    assert any(w.id == "django_edne_cep.W001" for w in warnings)


@pytest.mark.django_db
def test_check_warning_message():
    warnings = check_tables_exist(app_configs=None)
    cep_warning = next(w for w in warnings if w.id == "django_edne_cep.W001")
    assert "cep_unificado" in cep_warning.msg

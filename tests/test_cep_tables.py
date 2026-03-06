from django.db import models as django_models

from django_edne_cep.cep_tables import models as cep_models

MODEL_TABLE_MAP = {
    "Localidade": "log_localidade",
    "Bairro": "log_bairro",
    "CaixaPostalComunitaria": "log_cpc",
    "Logradouro": "log_logradouro",
    "GrandeUsuario": "log_grande_usuario",
    "UnidadeOperacional": "log_unid_oper",
}


def test_all_6_models_exist():
    for name in MODEL_TABLE_MAP:
        assert hasattr(cep_models, name), f"Missing model: {name}"


def test_all_models_unmanaged():
    for name in MODEL_TABLE_MAP:
        model = getattr(cep_models, name)
        assert model._meta.managed is False, f"{name} should be unmanaged"


def test_all_models_correct_db_table():
    for name, table in MODEL_TABLE_MAP.items():
        model = getattr(cep_models, name)
        assert model._meta.db_table == table, f"{name}.db_table should be {table}"


def test_logradouro_has_cep_field():
    assert "cep" in {f.name for f in cep_models.Logradouro._meta.get_fields()}


def test_localidade_has_loc_nu_pk():
    assert cep_models.Localidade._meta.pk.name == "loc_nu"


def test_integer_pks_use_autofield():
    for name in MODEL_TABLE_MAP:
        model = getattr(cep_models, name)
        pk = model._meta.pk
        if isinstance(pk, django_models.IntegerField):
            assert isinstance(pk, django_models.AutoField), (
                f"{name}.pk should be AutoField, got {type(pk).__name__}"
            )


def test_bairro_has_fk_to_localidade():
    field = cep_models.Bairro._meta.get_field("loc_nu")
    assert isinstance(field, django_models.ForeignKey)
    assert field.related_model is cep_models.Localidade


def test_logradouro_has_fk_to_localidade():
    field = cep_models.Logradouro._meta.get_field("loc_nu")
    assert isinstance(field, django_models.ForeignKey)
    assert field.related_model is cep_models.Localidade


def test_logradouro_has_fk_to_bairro():
    field = cep_models.Logradouro._meta.get_field("bai_nu_ini")
    assert isinstance(field, django_models.ForeignKey)
    assert field.related_model is cep_models.Bairro


def test_removed_models_not_present():
    removed = [
        "FaixaUf",
        "VarLoc",
        "FaixaLocalidade",
        "VarBai",
        "FaixaBairro",
        "FaixaCpc",
        "VarLog",
        "NumSec",
        "FaixaUop",
        "Pais",
    ]
    for name in removed:
        assert not hasattr(cep_models, name), f"{name} should not exist in cep_tables"

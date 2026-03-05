from django_edne_cep.cep_tables import models as cep_models

MODEL_TABLE_MAP = {
    "FaixaUf": "log_faixa_uf",
    "Localidade": "log_localidade",
    "VarLoc": "log_var_loc",
    "FaixaLocalidade": "log_faixa_localidade",
    "Bairro": "log_bairro",
    "VarBai": "log_var_bai",
    "FaixaBairro": "log_faixa_bairro",
    "CaixaPostalComunitaria": "log_cpc",
    "FaixaCpc": "log_faixa_cpc",
    "Logradouro": "log_logradouro",
    "VarLog": "log_var_log",
    "NumSec": "log_num_sec",
    "GrandeUsuario": "log_grande_usuario",
    "UnidadeOperacional": "log_unid_oper",
    "FaixaUop": "log_faixa_uop",
    "Pais": "ect_pais",
}


def test_all_16_models_exist():
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


def test_pais_has_pai_sg_pk():
    assert cep_models.Pais._meta.pk.name == "pai_sg"

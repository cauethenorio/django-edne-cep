from django_edne_cep.models import Cep


def test_cep_model_meta():
    assert Cep._meta.managed is False
    assert Cep._meta.db_table == "cep_unificado"


def test_cep_model_pk():
    assert Cep._meta.pk.name == "cep"


def test_cep_model_fields():
    field_names = {f.name for f in Cep._meta.get_fields()}
    expected = {
        "cep",
        "logradouro",
        "complemento",
        "bairro",
        "municipio",
        "municipio_cod_ibge",
        "uf",
        "nome",
    }
    assert field_names == expected


def test_cep_str():
    cep = Cep(cep="01001000", municipio="São Paulo", uf="SP")
    assert str(cep) == "01001000"

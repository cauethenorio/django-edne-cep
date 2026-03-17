from django_edne_cep.models import Cep


def test_cep_model_meta():
    assert Cep._meta.managed is False
    assert Cep._meta.db_table == "edne_cep"


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
    assert str(cep) == "01001-000"


def test_cep_formatado():
    cep = Cep(cep="01001000")
    assert cep.cep_formatado == "01001-000"


def test_as_dict_full():
    cep = Cep(
        cep="01001000",
        logradouro="Praça da Sé",
        complemento="lado ímpar",
        bairro="Sé",
        municipio="São Paulo",
        municipio_cod_ibge=3550308,
        uf="SP",
        nome="",
    )
    assert cep.as_dict() == {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "complemento": "lado ímpar",
        "bairro": "Sé",
        "municipio": "São Paulo",
        "municipio_cod_ibge": 3550308,
        "uf": "SP",
        "nome": "",
    }


def test_as_dict_nullable_fields():
    cep = Cep(
        cep="18170000",
        municipio="Piedade",
        municipio_cod_ibge=3537800,
        uf="SP",
    )
    result = cep.as_dict()
    assert result["cep"] == "18170-000"
    assert result["logradouro"] is None
    assert result["bairro"] is None
    assert result["municipio"] == "Piedade"

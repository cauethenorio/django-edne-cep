import pytest
from django.core.exceptions import ValidationError

from django_edne_cep.forms import CepFormField
from django_edne_cep.models import Cep


@pytest.fixture()
def cep_in_db(_cep_table, db):
    """Insert a CEP into the test database and return it."""
    return Cep.objects.create(
        cep="01001000",
        logradouro="Praça da Sé",
        bairro="Sé",
        municipio="São Paulo",
        municipio_cod_ibge=3550308,
        uf="SP",
    )


class TestCepFormField:
    def test_returns_cep_instance(self, cep_in_db):
        field = CepFormField()
        result = field.clean("01001000")
        assert isinstance(result, Cep)
        assert result.cep == "01001000"

    def test_normalizes_hyphen(self, cep_in_db):
        field = CepFormField()
        result = field.clean("01001-000")
        assert isinstance(result, Cep)
        assert result.cep == "01001000"

    def test_strips_whitespace(self, cep_in_db):
        field = CepFormField()
        result = field.clean("  01001-000  ")
        assert isinstance(result, Cep)

    def test_raises_on_nonexistent_cep(self, _cep_table, db):
        field = CepFormField()
        with pytest.raises(ValidationError) as exc_info:
            field.clean("99999999")
        assert exc_info.value.code == "cep_not_found"

    def test_raises_on_invalid_format(self):
        field = CepFormField()
        with pytest.raises(ValidationError):
            field.clean("1234")

    def test_empty_required(self):
        field = CepFormField(required=True)
        with pytest.raises(ValidationError):
            field.clean("")

    def test_empty_not_required(self):
        field = CepFormField(required=False)
        result = field.clean("")
        assert result is None

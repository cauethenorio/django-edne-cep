import pytest
from django.test import override_settings

from django_edne_cep.models import Cep
from django_edne_cep.services import lookup_cep


@pytest.mark.django_db
@pytest.mark.usefixtures("_create_unmanaged_tables")
def test_lookup_cep_not_found():
    result = lookup_cep("99999999")
    assert result is None


@pytest.mark.django_db
def test_lookup_cep_strips_hyphen(mocker):
    mock_filter = mocker.patch.object(
        Cep.objects, "filter", return_value=mocker.MagicMock(first=lambda: None)
    )
    lookup_cep("01001-000")
    mock_filter.assert_called_once_with(cep="01001000")


@pytest.mark.django_db
def test_lookup_cep_strips_whitespace(mocker):
    mock_filter = mocker.patch.object(
        Cep.objects, "filter", return_value=mocker.MagicMock(first=lambda: None)
    )
    lookup_cep("  01001000  ")
    mock_filter.assert_called_once_with(cep="01001000")


@pytest.mark.django_db
def test_lookup_cep_uses_cache(mocker):
    sentinel = Cep(cep="01001000", municipio="São Paulo", uf="SP")
    mocker.patch.object(
        Cep.objects,
        "filter",
        return_value=mocker.MagicMock(first=lambda: sentinel),
    )
    cache_set = mocker.patch("django.core.cache.cache.set")

    result = lookup_cep("01001000")

    assert result is sentinel
    cache_set.assert_called_once()


@override_settings(EDNE_CEP={"CACHE_TIMEOUT": 0})
@pytest.mark.django_db
def test_lookup_cep_skips_cache_when_timeout_zero(mocker):
    mocker.patch.object(
        Cep.objects,
        "filter",
        return_value=mocker.MagicMock(first=lambda: None),
    )
    cache_get = mocker.patch("django.core.cache.cache.get")

    lookup_cep("01001000")

    cache_get.assert_not_called()

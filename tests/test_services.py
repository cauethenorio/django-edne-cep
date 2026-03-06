import pytest
from django.core.cache import caches
from django.test import override_settings

from django_edne_cep.models import Cep
from django_edne_cep.services import lookup_cep


@pytest.fixture(autouse=True)
def _clear_cache():
    """Clear the default cache before each test to avoid cross-test contamination."""
    caches["default"].clear()
    yield
    caches["default"].clear()


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
    cache = caches["default"]
    cache_set = mocker.patch.object(cache, "set")

    result = lookup_cep("01001000")

    assert result is sentinel
    cache_set.assert_called_once()


@pytest.mark.django_db
def test_lookup_cep_caches_none_on_miss(mocker):
    mocker.patch.object(
        Cep.objects,
        "filter",
        return_value=mocker.MagicMock(first=lambda: None),
    )
    cache = caches["default"]
    cache_set = mocker.patch.object(cache, "set")

    result = lookup_cep("99999999")

    assert result is None
    cache_set.assert_called_once_with("edne:cep:99999999", None, 3600)


@pytest.mark.django_db
def test_lookup_cep_returns_cached_none_without_db_hit(mocker):
    cache = caches["default"]
    cache.set("edne:cep:99999999", None, 3600)

    mock_filter = mocker.patch.object(Cep.objects, "filter")

    result = lookup_cep("99999999")

    assert result is None
    mock_filter.assert_not_called()


@pytest.mark.django_db
def test_lookup_cep_cache_hit_skips_db(mocker):
    sentinel = Cep(cep="01001000", municipio="São Paulo", uf="SP")
    caches["default"].set("edne:cep:01001000", sentinel, 3600)

    mock_filter = mocker.patch.object(Cep.objects, "filter")

    result = lookup_cep("01001000")

    assert result.cep == "01001000"
    assert result.municipio == "São Paulo"
    mock_filter.assert_not_called()


@override_settings(EDNE_CEP={"CACHE_TIMEOUT": 0})
@pytest.mark.django_db
def test_lookup_cep_skips_cache_when_timeout_zero(mocker):
    mocker.patch.object(
        Cep.objects,
        "filter",
        return_value=mocker.MagicMock(first=lambda: None),
    )
    cache = caches["default"]
    cache_get = mocker.patch.object(cache, "get")

    lookup_cep("01001000")

    cache_get.assert_not_called()


@override_settings(
    EDNE_CEP={"CACHE_ALIAS": "secondary"},
    CACHES={
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
        "secondary": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "secondary",
        },
    },
)
@pytest.mark.django_db
def test_lookup_cep_uses_configured_cache_alias(mocker):
    sentinel = Cep(cep="01001000", municipio="São Paulo", uf="SP")
    mocker.patch.object(
        Cep.objects,
        "filter",
        return_value=mocker.MagicMock(first=lambda: sentinel),
    )
    secondary_cache = caches["secondary"]
    cache_set = mocker.patch.object(secondary_cache, "set")

    lookup_cep("01001000")

    cache_set.assert_called_once()


@pytest.mark.django_db
@pytest.mark.usefixtures("_create_unmanaged_tables")
def test_lookup_cep_returns_instance_from_db():
    Cep.objects.create(
        cep="01001000",
        logradouro="Praça da Sé",
        bairro="Sé",
        municipio="São Paulo",
        municipio_cod_ibge=3550308,
        uf="SP",
    )

    result = lookup_cep("01001-000")

    assert isinstance(result, Cep)
    assert result.cep == "01001000"
    assert result.municipio == "São Paulo"


def test_lookup_cep_importable_via_package():
    """Verify lazy import works: importing from django_edne_cep doesn't fail."""
    from django_edne_cep import lookup_cep as fn  # noqa: PLC0415

    assert callable(fn)

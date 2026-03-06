import pytest
from django.core.management import call_command
from django.test import override_settings
from edne_correios_loader import TableSetEnum


@pytest.fixture()
def mock_loader(mocker):
    cls = mocker.patch(
        "django_edne_cep.management.commands.load_edne_cep.DneLoaderWithProgress"
    )
    cls.return_value = mocker.MagicMock()
    return cls


@override_settings(INSTALLED_APPS=["django_edne_cep"])
@pytest.mark.django_db
def test_load_edne_cep_default(mock_loader):
    call_command("load_edne_cep")

    mock_loader.assert_called_once()
    assert mock_loader.call_args.kwargs["dne_source"] is None
    mock_loader.return_value.load.assert_called_once_with(TableSetEnum.UNIFIED_CEP_ONLY)


@pytest.mark.django_db
def test_load_edne_cep_with_source(mock_loader):
    edne_path = "/tmp/edne.zip"  # noqa: S108
    call_command("load_edne_cep", edne_source=edne_path)

    assert mock_loader.call_args.kwargs["dne_source"] == edne_path


@override_settings(INSTALLED_APPS=["django_edne_cep", "django_edne_cep.cep_tables"])
@pytest.mark.django_db
def test_load_edne_cep_infers_cep_tables_when_installed(mock_loader):
    call_command("load_edne_cep")

    mock_loader.return_value.load.assert_called_once_with(TableSetEnum.CEP_TABLES)


@override_settings(EDNE_CEP={"TABLE_SET": "all"})
@pytest.mark.django_db
def test_load_edne_cep_explicit_table_set(mock_loader):
    call_command("load_edne_cep")

    mock_loader.return_value.load.assert_called_once_with(TableSetEnum.ALL_TABLES)


@pytest.mark.parametrize(
    ("engine", "expected_scheme"),
    [
        ("django.db.backends.postgresql", "postgresql"),
        ("django.db.backends.mysql", "mysql"),
        ("django.contrib.gis.db.backends.postgis", "postgresql"),
        ("django.contrib.gis.db.backends.spatialite", "sqlite"),
        ("django.contrib.gis.db.backends.mysql", "mysql"),
    ],
)
@pytest.mark.django_db
def test_get_database_url_supports_extra_backends(mock_loader, engine, expected_scheme):
    db_config = {
        "ENGINE": engine,
        "NAME": "testdb",
        "USER": "u",
        "PASSWORD": "p",
        "HOST": "localhost",
        "PORT": "5432",
    }
    with override_settings(DATABASES={"default": db_config}):
        call_command("load_edne_cep")

    url = mock_loader.call_args.kwargs["database_url"]
    assert url.startswith(f"{expected_scheme}://")

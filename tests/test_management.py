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
# safe to override DATABASES: loader is mocked, no real DB connection is used
@pytest.mark.filterwarnings("ignore::UserWarning")
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


@override_settings(EDNE_CEP={"DATABASE_URL": "postgresql://custom:5432/mydb"})
@pytest.mark.django_db
def test_get_database_url_uses_explicit_setting(mock_loader):
    call_command("load_edne_cep")

    assert (
        mock_loader.call_args.kwargs["database_url"] == "postgresql://custom:5432/mydb"
    )


# safe to override DATABASES: loader is mocked, no real DB connection is used
@pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.django_db
def test_get_database_url_sqlite(mock_loader):
    db_config = {"ENGINE": "django.db.backends.sqlite3", "NAME": "/tmp/test.db"}  # noqa: S108
    with override_settings(DATABASES={"default": db_config}):
        call_command("load_edne_cep")

    assert mock_loader.call_args.kwargs["database_url"] == "sqlite:////tmp/test.db"


# safe to override DATABASES: loader is mocked, no real DB connection is used
@pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.django_db
def test_get_database_url_postgresql_full(mock_loader):
    db_config = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "USER": "admin",
        "PASSWORD": "secret",
        "HOST": "db.example.com",
        "PORT": "5433",
    }
    with override_settings(DATABASES={"default": db_config}):
        call_command("load_edne_cep")

    assert mock_loader.call_args.kwargs["database_url"] == (
        "postgresql://admin:secret@db.example.com:5433/mydb"
    )


# safe to override DATABASES: loader is mocked, no real DB connection is used
@pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.django_db
def test_get_database_url_postgresql_no_port(mock_loader):
    db_config = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "USER": "admin",
        "PASSWORD": "secret",
        "HOST": "localhost",
        "PORT": "",
    }
    with override_settings(DATABASES={"default": db_config}):
        call_command("load_edne_cep")

    assert mock_loader.call_args.kwargs["database_url"] == (
        "postgresql://admin:secret@localhost/mydb"
    )


# safe to override DATABASES: loader is mocked, no real DB connection is used
@pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.django_db
@pytest.mark.usefixtures("mock_loader")
def test_get_database_url_unsupported_engine_raises():
    db_config = {"ENGINE": "some.custom.backend", "NAME": "mydb"}
    with override_settings(DATABASES={"default": db_config}):
        with pytest.raises(ValueError, match="Unsupported database engine"):
            call_command("load_edne_cep")

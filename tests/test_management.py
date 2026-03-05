from unittest.mock import MagicMock

import pytest
from django.core.management import call_command
from django.test import override_settings
from edne_correios_loader import TableSetEnum


@override_settings(INSTALLED_APPS=["django_edne_cep"])
@pytest.mark.django_db
def test_load_dne_default(mocker):
    mock_loader_cls = mocker.patch(
        "django_edne_cep.management.commands.load_dne.DneLoader"
    )
    mock_loader = MagicMock()
    mock_loader_cls.return_value = mock_loader

    call_command("load_dne")

    mock_loader_cls.assert_called_once()
    call_kwargs = mock_loader_cls.call_args
    assert call_kwargs.kwargs["dne_source"] is None
    mock_loader.load.assert_called_once_with(TableSetEnum.UNIFIED_CEP_ONLY)


@pytest.mark.django_db
def test_load_dne_with_source(mocker):
    mock_loader_cls = mocker.patch(
        "django_edne_cep.management.commands.load_dne.DneLoader"
    )
    mock_loader = MagicMock()
    mock_loader_cls.return_value = mock_loader

    dne_path = "/tmp/edne.zip"  # noqa: S108
    call_command("load_dne", dne_source=dne_path)

    call_kwargs = mock_loader_cls.call_args
    assert call_kwargs.kwargs["dne_source"] == dne_path


@override_settings(INSTALLED_APPS=["django_edne_cep", "django_edne_cep.cep_tables"])
@pytest.mark.django_db
def test_load_dne_infers_cep_tables_when_installed(mocker):
    mock_loader_cls = mocker.patch(
        "django_edne_cep.management.commands.load_dne.DneLoader"
    )
    mock_loader = MagicMock()
    mock_loader_cls.return_value = mock_loader

    call_command("load_dne")

    mock_loader.load.assert_called_once_with(TableSetEnum.CEP_TABLES)


@override_settings(EDNE_CEP={"TABLE_SET": "all"})
@pytest.mark.django_db
def test_load_dne_explicit_table_set(mocker):
    mock_loader_cls = mocker.patch(
        "django_edne_cep.management.commands.load_dne.DneLoader"
    )
    mock_loader = MagicMock()
    mock_loader_cls.return_value = mock_loader

    call_command("load_dne")

    mock_loader.load.assert_called_once_with(TableSetEnum.ALL_TABLES)

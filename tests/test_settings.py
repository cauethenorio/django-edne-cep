import pytest
from django.test import override_settings

from django_edne_cep.settings import DEFAULTS, get_setting


def test_get_setting_returns_default():
    assert get_setting("CACHE_TIMEOUT") == 3600


def test_get_setting_returns_default_for_all_keys():
    for key, value in DEFAULTS.items():
        assert get_setting(key) == value


@override_settings(EDNE_CEP={"CACHE_TIMEOUT": 7200})
def test_get_setting_returns_override():
    assert get_setting("CACHE_TIMEOUT") == 7200


def test_get_setting_raises_for_unknown_key():

    with pytest.raises(KeyError, match="UNKNOWN"):
        get_setting("UNKNOWN")

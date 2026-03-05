from django.conf import settings

DEFAULTS = {
    "TABLE_NAMES": {},
    "TABLE_SET": None,
    "DNE_SOURCE": None,
    "DATABASE_ALIAS": "default",
    "DATABASE_URL": None,
    "CACHE_TIMEOUT": 3600,
    "CACHE_ALIAS": "default",
}


def get_setting(key):
    if key not in DEFAULTS:
        msg = f"Unknown django-edne-cep setting: {key}"
        raise KeyError(msg)

    user_settings = getattr(settings, "EDNE_CEP", {})
    return user_settings.get(key, DEFAULTS[key])

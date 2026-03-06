from typing import Any

from django.conf import settings

DEFAULTS: dict[str, Any] = {
    "TABLE_NAMES": {
        "cep_unificado": "edne_cep",
        "log_localidade": "edne_localidade",
        "log_bairro": "edne_bairro",
        "log_cpc": "edne_caixa_postal",
        "log_logradouro": "edne_logradouro",
        "log_grande_usuario": "edne_grande_usuario",
        "log_unid_oper": "edne_unidade_operacional",
    },
    "TABLE_SET": None,
    "EDNE_SOURCE": None,
    "DATABASE_ALIAS": "default",
    "DATABASE_URL": None,
    "CACHE_TIMEOUT": 3600,
    "CACHE_ALIAS": "default",
}


def get_setting(key: str) -> Any:
    if key not in DEFAULTS:
        msg = f"Unknown django-edne-cep setting: {key}"
        raise KeyError(msg)

    user_settings = getattr(settings, "EDNE_CEP", {})
    return user_settings.get(key, DEFAULTS[key])

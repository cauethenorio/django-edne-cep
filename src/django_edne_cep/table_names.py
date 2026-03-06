from edne_correios_loader.tables import make_table_name_fn

from .settings import DEFAULTS, get_setting


def get_table_name(original_name: str) -> str:
    user_value = get_setting("TABLE_NAMES")
    defaults = DEFAULTS["TABLE_NAMES"]

    if callable(user_value) and not isinstance(user_value, dict):
        resolver = user_value
    elif isinstance(user_value, dict):
        resolver = {**defaults, **user_value}
    else:
        resolver = defaults

    fn = make_table_name_fn(resolver or None)
    return fn(original_name)

from edne_correios_loader.tables import make_table_name_fn

from .settings import get_setting


def get_table_name(original_name: str) -> str:
    resolver = get_setting("TABLE_NAMES") or None
    fn = make_table_name_fn(resolver)
    return fn(original_name)

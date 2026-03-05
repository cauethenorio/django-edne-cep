from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from edne_correios_loader import DneLoader, TableSetEnum

from django_edne_cep.settings import get_setting


def _get_database_url():
    url = get_setting("DATABASE_URL")
    if url:
        return url

    alias = get_setting("DATABASE_ALIAS")
    db = settings.DATABASES[alias]
    engine = db["ENGINE"]

    engine_map = {
        "django.db.backends.sqlite3": "sqlite",
        "django.db.backends.postgresql": "postgresql",
        "django.db.backends.mysql": "mysql",
    }

    dialect = engine_map.get(engine)
    if dialect is None:
        msg = (
            f"Unsupported database engine: {engine}. "
            "Set EDNE_CEP['DATABASE_URL'] directly."
        )
        raise ValueError(msg)

    if dialect == "sqlite":
        name = db.get("NAME", ":memory:")
        return f"sqlite:///{name}"

    user = db.get("USER", "")
    password = db.get("PASSWORD", "")
    host = db.get("HOST", "localhost")
    port = db.get("PORT", "")
    name = db["NAME"]

    auth = f"{user}:{password}@" if user else ""
    port_str = f":{port}" if port else ""

    return f"{dialect}://{auth}{host}{port_str}/{name}"


def _get_table_set():
    explicit = get_setting("TABLE_SET")
    if explicit is not None:
        return TableSetEnum(explicit)

    if apps.is_installed("django_edne_cep.cep_tables"):
        return TableSetEnum.CEP_TABLES

    return TableSetEnum.UNIFIED_CEP_ONLY


class Command(BaseCommand):
    help = "Load Correios eDNE data into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dne-source",
            type=str,
            default=None,
            help="Path or URL to eDNE zip file (default: auto-download)",
        )

    def handle(self, *_args, **options):
        dne_source = options["dne_source"] or get_setting("DNE_SOURCE")
        table_names = get_setting("TABLE_NAMES") or None
        database_url = _get_database_url()
        table_set = _get_table_set()

        self.stdout.write(f"Loading eDNE data (table_set={table_set.value})...")

        loader = DneLoader(
            database_url=database_url,
            dne_source=dne_source,
            table_names=table_names,
        )
        loader.load(table_set)

        self.stdout.write(self.style.SUCCESS("eDNE data loaded successfully."))

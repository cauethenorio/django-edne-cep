import logging

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from edne_correios_loader import TableSetEnum
from edne_correios_loader.cli import DneLoaderWithProgress
from edne_correios_loader.cli.logger import configure_logger

from django_edne_cep.settings import get_setting

_VERBOSITY_TO_LOG_LEVEL = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
    3: logging.DEBUG,
}


class Command(BaseCommand):
    help = "Load Correios eDNE CEP into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--edne-source",
            type=str,
            default=None,
            help="Path or URL to eDNE zip file (default: auto-download)",
        )

    def handle(self, *_args, **options):
        self._configure_logging(options["verbosity"])

        edne_source = options["edne_source"] or get_setting("EDNE_SOURCE")
        table_names = get_setting("TABLE_NAMES")
        database_url = _get_database_url()
        table_set = _get_table_set()

        self.stdout.write(f"Loading eDNE CEP (table_set={table_set.value})...\n")

        loader = DneLoaderWithProgress(
            database_url=database_url,
            dne_source=edne_source,
            table_names=table_names,
        )
        loader.load(table_set)

        self.stdout.write(self.style.SUCCESS("eDNE CEP loaded successfully."))

    def _configure_logging(self, verbosity):
        """Map Django's verbosity flag to edne_correios_loader log level"""
        level = _VERBOSITY_TO_LOG_LEVEL.get(verbosity, logging.INFO)

        # reuse edne_correios_loader's colored formatter for consistent output
        logger = logging.getLogger("edne_correios_loader")
        configure_logger(logger)
        logger.setLevel(level)


def _get_database_url() -> str:
    """Build a database URL from Django's DATABASES setting"""
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
        "django.contrib.gis.db.backends.spatialite": "sqlite",
        "django.contrib.gis.db.backends.postgis": "postgresql",
        "django.contrib.gis.db.backends.mysql": "mysql",
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


def _get_table_set() -> TableSetEnum:
    """Determine which table set to load based on settings and installed apps"""
    explicit = get_setting("TABLE_SET")
    if explicit is not None:
        return TableSetEnum(explicit)

    if apps.is_installed("django_edne_cep.cep_tables"):
        return TableSetEnum.CEP_TABLES

    return TableSetEnum.UNIFIED_CEP_ONLY

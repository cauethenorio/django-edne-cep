import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import connection
from django.test import Client

from django_edne_cep.admin import CepAdmin
from django_edne_cep.cep_tables import models as cep_models
from django_edne_cep.cep_tables.admin import CEP_TABLES_ADMINS
from django_edne_cep.models import Cep
from tests.conftest import CREATE_CEP_TABLE_SQL

CREATE_CEP_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS edne_localidade (
        loc_nu INTEGER PRIMARY KEY AUTOINCREMENT,
        ufe_sg VARCHAR(2) NOT NULL,
        loc_no VARCHAR(72) NOT NULL,
        cep VARCHAR(8),
        loc_in_sit VARCHAR(1) NOT NULL,
        loc_in_tipo_loc VARCHAR(1) NOT NULL,
        loc_nu_sub INTEGER,
        loc_no_abrev VARCHAR(36),
        mun_nu INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS edne_bairro (
        bai_nu INTEGER PRIMARY KEY AUTOINCREMENT,
        ufe_sg VARCHAR(2) NOT NULL,
        loc_nu INTEGER NOT NULL,
        bai_no VARCHAR(72) NOT NULL,
        bai_no_abrev VARCHAR(36)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS edne_logradouro (
        log_nu INTEGER PRIMARY KEY AUTOINCREMENT,
        ufe_sg VARCHAR(2) NOT NULL,
        loc_nu INTEGER NOT NULL,
        bai_nu_ini INTEGER NOT NULL,
        bai_nu_fim INTEGER,
        log_no VARCHAR(100) NOT NULL,
        log_complemento VARCHAR(100),
        cep VARCHAR(8) NOT NULL,
        tlo_tx VARCHAR(36) NOT NULL,
        log_sta_tlo VARCHAR(1),
        log_no_abrev VARCHAR(36)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS edne_caixa_postal (
        cpc_nu INTEGER PRIMARY KEY AUTOINCREMENT,
        ufe_sg VARCHAR(2) NOT NULL,
        loc_nu INTEGER NOT NULL,
        cpc_no VARCHAR(72) NOT NULL,
        cpc_endereco VARCHAR(100) NOT NULL,
        cep VARCHAR(8) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS edne_grande_usuario (
        gru_nu INTEGER PRIMARY KEY AUTOINCREMENT,
        ufe_sg VARCHAR(2) NOT NULL,
        loc_nu INTEGER NOT NULL,
        bai_nu INTEGER NOT NULL,
        log_nu INTEGER,
        gru_no VARCHAR(72) NOT NULL,
        gru_endereco VARCHAR(100) NOT NULL,
        cep VARCHAR(8) NOT NULL,
        gru_no_abrev VARCHAR(36)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS edne_unidade_operacional (
        uop_nu INTEGER PRIMARY KEY AUTOINCREMENT,
        ufe_sg VARCHAR(2) NOT NULL,
        loc_nu INTEGER NOT NULL,
        bai_nu INTEGER NOT NULL,
        log_nu INTEGER,
        uop_no VARCHAR(100) NOT NULL,
        uop_endereco VARCHAR(100) NOT NULL,
        cep VARCHAR(8) NOT NULL,
        uop_in_cp VARCHAR(1),
        uop_no_abrev VARCHAR(36)
    )
    """,
]


@pytest.fixture(autouse=True)
def _admin_settings(settings):
    """Add admin, sessions, messages apps and configure middleware/templates."""
    settings.INSTALLED_APPS = [
        *settings.INSTALLED_APPS,
        "django.contrib.admin",
        "django.contrib.sessions",
        "django.contrib.messages",
    ]
    # cache-backed sessions so we don't need the django_session table
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    settings.MIDDLEWARE = [
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]
    settings.TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]
    settings.ROOT_URLCONF = "tests.urls"


@pytest.fixture(scope="session")
def _all_tables(django_db_setup, django_db_blocker):  # noqa: ARG001
    """Create all unmanaged model tables for admin view tests."""
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CEP_TABLE_SQL)
            for sql in CREATE_CEP_TABLES_SQL:
                cursor.execute(sql)


@pytest.fixture(autouse=True)
def _register_admin(_all_tables):
    """Register all admin models for URL resolution, clean up after test."""
    site = admin.site
    registered = []

    if Cep not in site._registry:
        site.register(Cep, CepAdmin)
        registered.append(Cep)

    for model_name, admin_class in CEP_TABLES_ADMINS.items():
        model = getattr(cep_models, model_name)
        if model not in site._registry:
            site.register(model, admin_class)
            registered.append(model)

    yield

    for model in registered:
        if model in site._registry:
            site.unregister(model)


@pytest.fixture()
def admin_client():
    user = User.objects.create_superuser("admin", "", "admin")
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture()
def sample_cep_data():
    """Minimal CEP rows for testing the main Cep admin."""
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT OR IGNORE INTO edne_cep"
            " (cep, logradouro, bairro, municipio, municipio_cod_ibge, uf)"
            " VALUES ('01001000', 'Rua Teste', 'Centro', 'São Paulo', 3550308, 'SP')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO edne_cep"
            " (cep, municipio, municipio_cod_ibge, uf)"
            " VALUES ('18170001', 'Piedade', 3537800, 'SP')"
        )
    yield
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM edne_cep")


@pytest.fixture()
def sample_cep_tables_data():
    """Minimal rows across cep_tables models for testing their admin views."""
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT OR IGNORE INTO edne_localidade"
            " (loc_nu, ufe_sg, loc_no, cep, loc_in_sit, loc_in_tipo_loc)"
            " VALUES (1, 'SP', 'São Paulo', '01000000', '1', 'M')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO edne_bairro"
            " (bai_nu, ufe_sg, loc_nu, bai_no)"
            " VALUES (1, 'SP', 1, 'Centro')"
        )
        cursor.execute(
            "INSERT OR IGNORE INTO edne_logradouro"
            " (log_nu, ufe_sg, loc_nu, bai_nu_ini, log_no, cep, tlo_tx)"
            " VALUES (1, 'SP', 1, 1, 'Rua Teste', '01001000', 'Rua')"
        )
    yield
    with connection.cursor() as cursor:
        for table in [
            "edne_logradouro",
            "edne_bairro",
            "edne_localidade",
        ]:
            cursor.execute(f"DELETE FROM {table}")  # noqa: S608

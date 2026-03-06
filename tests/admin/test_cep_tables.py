"""
Test cep_tables admin views render correctly across Django versions.

Uses the Django test client to hit actual admin URLs, ensuring
list views, detail views, search, and filters all work.
"""

import pytest

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("sample_cep_tables_data"),
]


# -- Localidade --


def test_localidade_changelist(admin_client):
    response = admin_client.get("/admin/django_edne_cep/localidade/")
    assert response.status_code == 200
    assert "São Paulo" in response.content.decode()


def test_localidade_detail_has_related_links(admin_client):
    response = admin_client.get("/admin/django_edne_cep/localidade/1/change/")
    assert response.status_code == 200
    content = response.content.decode()
    assert "Ver" in content or "Nenhum" in content


def test_localidade_add_returns_403(admin_client):
    response = admin_client.get("/admin/django_edne_cep/localidade/add/")
    assert response.status_code == 403


# -- Bairro --


def test_bairro_changelist(admin_client):
    response = admin_client.get("/admin/django_edne_cep/bairro/")
    assert response.status_code == 200
    assert "Centro" in response.content.decode()


# -- Logradouro --


def test_logradouro_changelist(admin_client):
    response = admin_client.get("/admin/django_edne_cep/logradouro/")
    assert response.status_code == 200
    assert "Rua Teste" in response.content.decode()


def test_logradouro_search_by_localidade(admin_client):
    response = admin_client.get("/admin/django_edne_cep/logradouro/?q=São+Paulo")
    assert response.status_code == 200
    assert "Rua Teste" in response.content.decode()


def test_logradouro_filter_by_loc_nu(admin_client):
    response = admin_client.get("/admin/django_edne_cep/logradouro/?loc_nu=1")
    assert response.status_code == 200
    assert "Rua Teste" in response.content.decode()

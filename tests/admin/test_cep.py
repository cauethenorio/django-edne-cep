"""
Test Cep admin views render correctly across Django versions.

Uses the Django test client to hit actual admin URLs, ensuring
list views, search, and filters all work.
"""

import pytest

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("sample_cep_data")]


def test_changelist(admin_client):
    response = admin_client.get("/admin/django_edne_cep/cep/")
    assert response.status_code == 200
    assert "01001-000" in response.content.decode()


def test_search_with_hyphen(admin_client):
    response = admin_client.get("/admin/django_edne_cep/cep/?q=01001-000")
    assert response.status_code == 200
    assert "Rua Teste" in response.content.decode()


def test_search_without_hyphen(admin_client):
    response = admin_client.get("/admin/django_edne_cep/cep/?q=01001000")
    assert response.status_code == 200
    assert "Rua Teste" in response.content.decode()


def test_search_by_name(admin_client):
    """Search by street name should not strip hyphens."""
    response = admin_client.get("/admin/django_edne_cep/cep/?q=Rua+Teste")
    assert response.status_code == 200
    assert "01001-000" in response.content.decode()


def test_filter_by_uf(admin_client):
    response = admin_client.get("/admin/django_edne_cep/cep/?uf=SP")
    assert response.status_code == 200


def test_filter_tem_logradouro(admin_client):
    response = admin_client.get("/admin/django_edne_cep/cep/?tem_logradouro=yes")
    assert response.status_code == 200
    assert "Rua Teste" in response.content.decode()

    response = admin_client.get("/admin/django_edne_cep/cep/?tem_logradouro=no")
    assert response.status_code == 200
    assert "Piedade" in response.content.decode()


def test_column_is_sortable(admin_client):
    response = admin_client.get("/admin/django_edne_cep/cep/?o=1")
    assert response.status_code == 200


def test_add_returns_403(admin_client):
    response = admin_client.get("/admin/django_edne_cep/cep/add/")
    assert response.status_code == 403

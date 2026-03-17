import django_edne_cep


def test_all_exports_expected_names():
    expected = {"lookup_cep", "CepFormField", "validate_cep_format", "register_admin"}
    assert set(django_edne_cep.__all__) == expected


def test_all_names_are_importable():
    for name in django_edne_cep.__all__:
        attr = getattr(django_edne_cep, name)
        assert attr is not None, f"{name} resolved to None"
        assert callable(attr), f"{name} is not callable"

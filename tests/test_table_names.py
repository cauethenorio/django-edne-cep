from django.test import override_settings

from django_edne_cep.table_names import get_table_name


def test_default_table_name():
    assert get_table_name("cep_unificado") == "edne_cep"


def test_default_table_name_logradouro():
    assert get_table_name("log_logradouro") == "edne_logradouro"


@override_settings(EDNE_CEP={"TABLE_NAMES": {"cep_unificado": "my_cep"}})
def test_dict_override():
    assert get_table_name("cep_unificado") == "my_cep"


@override_settings(EDNE_CEP={"TABLE_NAMES": {"cep_unificado": "my_cep"}})
def test_dict_override_unmapped_keeps_default():
    assert get_table_name("log_logradouro") == "edne_logradouro"


@override_settings(EDNE_CEP={"TABLE_NAMES": {"log_logradouro": "log_logradouro"}})
def test_dict_override_can_restore_original_name():
    assert get_table_name("log_logradouro") == "log_logradouro"
    assert get_table_name("cep_unificado") == "edne_cep"


@override_settings(EDNE_CEP={"TABLE_NAMES": lambda name: f"dne_{name}"})
def test_callable_override():
    assert get_table_name("cep_unificado") == "dne_cep_unificado"
    assert get_table_name("log_logradouro") == "dne_log_logradouro"

import pytest
from django.core.exceptions import ValidationError

from django_edne_cep.validators import validate_cep_format


class TestValidateCepFormat:
    @pytest.mark.parametrize(
        "value",
        [
            "01001000",
            "12345678",
            "01001-000",
            "12345-678",
        ],
    )
    def test_accepts_valid_ceps(self, value):
        validate_cep_format(value)  # should not raise

    @pytest.mark.parametrize(
        "value",
        [
            "0100100",  # 7 digits
            "123456789",  # 9 digits
            "1234",  # too short
            "abcde-fgh",  # letters
            "01001 000",  # space instead of hyphen
            "01001--000",  # double hyphen
            "",  # empty
            "0100-1000",  # hyphen in wrong place
        ],
    )
    def test_rejects_invalid_ceps(self, value):
        with pytest.raises(ValidationError):
            validate_cep_format(value)

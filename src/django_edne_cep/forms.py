from django import forms
from django.core.exceptions import ValidationError

from .services import lookup_cep
from .validators import validate_cep_format


class CepFormField(forms.CharField):
    default_error_messages = {  # noqa: RUF012
        "cep_not_found": "CEP não encontrado.",
        "invalid_cep_format": "Formato de CEP inválido.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 9)  # "00000-000" = 9 chars
        kwargs.setdefault("min_length", 8)  # "00000000" = 8 chars
        kwargs.setdefault(
            "widget",
            forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "autocomplete": "postal-code",
                    "placeholder": "00000-000",
                }
            ),
        )
        super().__init__(**kwargs)
        self.validators.append(validate_cep_format)

    def clean(self, value):
        value = super().clean(value)
        if not value:
            return None
        result = lookup_cep(value)
        if result is None:
            raise ValidationError(
                self.error_messages["cep_not_found"],
                code="cep_not_found",
            )
        return result

from django.core.validators import RegexValidator

validate_cep_format = RegexValidator(
    regex=r"^\d{5}-?\d{3}$",
    message="Formato de CEP inválido.",
    code="invalid_cep_format",
)

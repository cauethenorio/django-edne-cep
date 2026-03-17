from importlib.metadata import version

__version__ = version("django-edne-cep")

__all__ = ["CepFormField", "lookup_cep", "register_admin", "validate_cep_format"]


def __getattr__(name):
    if name == "lookup_cep":
        from .services import lookup_cep  # noqa: PLC0415

        return lookup_cep
    if name == "CepFormField":
        from .forms import CepFormField  # noqa: PLC0415

        return CepFormField
    if name == "validate_cep_format":
        from .validators import validate_cep_format  # noqa: PLC0415

        return validate_cep_format
    if name == "register_admin":
        from .admin import register_admin  # noqa: PLC0415

        return register_admin
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)

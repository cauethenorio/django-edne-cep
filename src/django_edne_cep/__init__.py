def __getattr__(name):
    if name == "lookup_cep":
        from .services import lookup_cep  # noqa: PLC0415

        return lookup_cep
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)

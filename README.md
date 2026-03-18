*[Leia em Português](README.pt-BR.md)*

# django-edne-cep

[![PyPI version](https://img.shields.io/pypi/v/django-edne-cep.svg)](https://pypi.org/project/django-edne-cep/)
[![CI](https://github.com/cauethenorio/django-edne-cep/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/cauethenorio/django-edne-cep/actions/workflows/lint-and-test.yml)
[![Coverage](https://codecov.io/gh/cauethenorio/django-edne-cep/graph/badge.svg)](https://codecov.io/gh/cauethenorio/django-edne-cep)

Enables CEP (Brazilian postal code) lookups in your Django app backed by a local database.

Uses [edne-correios-loader](https://github.com/cauethenorio/edne-correios-loader) to populate the database from
Correios eDNE CEP data, eliminating dependency on external APIs.

<div align="center">
  <img src="https://raw.githubusercontent.com/cauethenorio/django-edne-cep/main/docs/images/cep-lookup.gif" />
    <p>HTMX-powered CEP lookup in the example app</p>
</div>

- One management command to download and load all 1.5M CEPs in your database
- Local database lookups, no external API calls, no network latency
- Leverages Django's cache to speed up repeated lookups
- Form field with CEP format validation and automatic address lookup
- Django admin integration (opt-in)
- Configurable table names, database alias, and cache backend

## Quick Start

**Step 1: Install**

```bash
pip install django-edne-cep
```

**Step 2: Add to `INSTALLED_APPS`**

```python
INSTALLED_APPS = [
    ...
    "django_edne_cep",
]
```

**Step 3: Load CEP data**

```bash
python manage.py load_edne_cep
```

This downloads the eDNE dataset from Correios (~350 MB) and populates the local database with all Brazilian CEPs.

**Use it:**

```python
from django_edne_cep import lookup_cep

cep = lookup_cep("01310-100")
if cep:
    print(f"{cep.logradouro}, {cep.municipio} - {cep.uf}")
    # "Avenida Paulista, São Paulo - SP"
```

## API Reference

### `def lookup_cep(cep_str: str) -> Cep | None`

Look up a CEP in the local database. Accepts both `"01310-100"` and `"01310100"` formats.

- Raises `ValidationError` for malformed input (not a valid CEP format).
- Returns `None` when the CEP is not found in the database (valid format, not in eDNE data).
- Results are cached using the configured cache backend.

```python
from django_edne_cep import lookup_cep
from django.core.exceptions import ValidationError

cep = lookup_cep("01310-100")  # accepts "01310-100" or "01310100"
if cep:
    print(f"{cep.logradouro}, {cep.municipio}/{cep.uf}")

try:
    lookup_cep("ABC")  # raises ValidationError for malformed input
except ValidationError:
    pass
```

The returned `Cep` instance has the following fields:

```python
cep.cep  # "01310100"  (8 digits, no hyphen)
cep.cep_formatado  # "01310-100" (property)
cep.logradouro  # str | None
cep.complemento  # str | None
cep.bairro  # str | None
cep.municipio  # str
cep.municipio_cod_ibge  # int
cep.uf  # str (2 chars, e.g. "SP")
cep.nome  # str | None
cep.as_dict()  # dict with all fields above
```

---

### `CepFormField`

A `CharField` subclass that validates CEP format and returns a `Cep` instance from `clean()`.

- Accepts `"00000000"` or `"00000-000"` input formats.
- Raises `ValidationError` with code `"cep_not_found"` when the CEP is not in the database.
- `form.cleaned_data["cep"]` is a `Cep` instance, not a string.

```python
from django import forms
from django_edne_cep import CepFormField


class EnderecoForm(forms.Form):
    cep = CepFormField()
    logradouro = forms.CharField(required=False)
    municipio = forms.CharField(required=False)


# In a view:
form = EnderecoForm(request.POST)
if form.is_valid():
    cep_obj = form.cleaned_data["cep"]  # Cep instance
    print(cep_obj.logradouro, cep_obj.municipio, cep_obj.uf)
```

---

### `validate_cep_format`

A Django `RegexValidator` that accepts `"00000000"` and `"00000-000"` formats. Raises `ValidationError` with code
`"invalid_cep_format"` on failure.

```python
from django_edne_cep import validate_cep_format

validate_cep_format("01310-100")  # passes silently
validate_cep_format("01310100")  # passes silently
validate_cep_format("ABC")  # raises ValidationError
```

Use it directly on any `CharField` or `Field` that should accept CEP values without triggering a database lookup.

---

## Configuration

All settings go in the `EDNE_CEP` dict in your Django settings file:

```python
EDNE_CEP = {
    "CACHE_TIMEOUT": 7200,
    "ADMIN_ENABLED": True,
}
```

| Setting          | Type          | Default     | Description                                           |
|------------------|---------------|-------------|-------------------------------------------------------|
| `TABLE_NAMES`    | `dict`        | see below   | Override individual eDNE table names                  |
| `TABLE_SET`      | `str \| None` | `None`      | Load only a subset of tables (e.g. `"cep"`)           |
| `EDNE_SOURCE`    | `str \| None` | `None`      | Path or URL to eDNE zip file; `None` prompts download |
| `DATABASE_ALIAS` | `str`         | `"default"` | Django database alias for CEP tables                  |
| `DATABASE_URL`   | `str \| None` | `None`      | Direct database URL (overrides `DATABASE_ALIAS`)      |
| `CACHE_TIMEOUT`  | `int`         | `3600`      | Cache TTL in seconds; `0` disables cache              |
| `CACHE_ALIAS`    | `str`         | `"default"` | Django cache alias for CEP lookups                    |
| `ADMIN_ENABLED`  | `bool`        | `False`     | Register CEP models in Django admin                   |

**Default `TABLE_NAMES`:**

```python
TABLE_NAMES = {
    "cep_unificado": "edne_cep",
    "log_localidade": "edne_localidade",
    "log_bairro": "edne_bairro",
    "log_cpc": "edne_caixa_postal",
    "log_logradouro": "edne_logradouro",
    "log_grande_usuario": "edne_grande_usuario",
    "log_unid_oper": "edne_unidade_operacional",
}
```

Override individual entries to map eDNE table names to your own table names.

## Admin

Enable the read-only Django admin for CEP data:

```python
# settings.py
EDNE_CEP = {
    "ADMIN_ENABLED": True,
}
```

The `CepAdmin` registers automatically when `django_edne_cep.admin` is imported. It supports full-text search by CEP,
street name, neighborhood, and municipality, plus filters by state (UF) and field presence.

For a custom `AdminSite`, call `register_admin(site=my_site)` explicitly after setting `ADMIN_ENABLED = True`.

![Admin Integration](https://raw.githubusercontent.com/cauethenorio/django-edne-cep/main/docs/images/admin.png)

## Example App

The `example/` directory contains a standalone Django project with an HTMX-powered CEP autofill form: type a CEP and the
address fields fill in automatically without a page reload.

See [example/README.md](example/README.md) for full instructions on running it locally.

## License

[MIT](LICENSE)

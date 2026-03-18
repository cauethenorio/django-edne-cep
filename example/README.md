# django-edne-cep example app

A Django project demonstrating CEP lookup with an HTMX-powered form that auto-fills address fields when a valid CEP is entered.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Steps

**1. From the repo root, change to the example directory:**

```bash
cd example
```

**2. Load CEP data:**

```bash
uv run python manage.py load_edne_cep --auto-download
```

The first run downloads the eDNE dataset from Correios (~350 MB) and populates the local SQLite database. Subsequent runs reuse the cached file.

**3. Start the development server:**

```bash
uv run python manage.py runserver
```

**4. Open the HTMX CEP lookup demo:**

```
http://localhost:8000/htmx/
```

**5. (Optional) Create a superuser for admin access:**

```bash
uv run python manage.py createsuperuser
```

Then visit `http://localhost:8000/admin/` to browse the CEP data with the read-only Django admin.

## What to Expect

Open `http://localhost:8000/htmx/` and type a CEP (e.g. `01310-100`) into the CEP field. As soon as a valid, known CEP is entered, the address fields (street, neighborhood, city, state) fill in automatically — no page reload required. This demonstrates `CepFormField` and `lookup_cep()` working together via an HTMX endpoint.

If the CEP is valid in format but not found in the database, the form shows a "CEP não encontrado" error. If the format is invalid, a format validation error is shown immediately.

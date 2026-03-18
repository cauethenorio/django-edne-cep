# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-17

### Added

- `lookup_cep()` service with cache support and stampede protection
- `Cep` unmanaged model with `as_dict()` and `cep_formatado` property
- `CepFormField` form field with CEP format validation and automatic database lookup (returns `Cep` instance)
- `validate_cep_format` regex validator accepting `00000000` and `00000-000` formats
- `register_admin()` opt-in admin registration with read-only `CepAdmin`
- `load_edne_cep` management command with colored logging and progress bar
- `cep_tables` sub-app with all 16 eDNE table models (unmanaged)
- System checks for missing database tables
- Configurable table names, cache backend, database alias, and database URL via `EDNE_CEP` settings dict
- Example app with HTMX-powered CEP autofill form

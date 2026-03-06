# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `lookup_cep()` service with cache support
- `Cep` unmanaged model
- `load_edne_cep` management command with colored logging and progress bar
- `cep_tables` sub-app with all 16 eDNE table models
- System checks for missing tables
- Configurable table names, cache, and database settings

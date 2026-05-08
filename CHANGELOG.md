# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-08

### Added
- Initial public release of `ckanext-filterview`, a fork/extension of the
  official `ckanext-datatablesview` plugin.
- Comparison operators (`=`, `!=`, `>`, `>=`, `<`, `<=`) on numeric and
  date/timestamp columns.
- `is empty` / `is not empty` filters.
- Client-side filtering mode with configurable `client_side_max_rows`
  (default 10,000).
- Server-side filtering mode preserved for compatibility with the upstream
  `datatablesview`.
- Filtered export to CSV, JSON, and XML.
- Standard CKAN extension packaging: `pyproject.toml`, `LICENSE`
  (AGPL-3.0), `requirements.txt`.
- Dockerised development environment under `dev/`.

[Unreleased]: https://github.com/Wenze-Zhang/ckanext-filterview/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Wenze-Zhang/ckanext-filterview/releases/tag/v0.1.0

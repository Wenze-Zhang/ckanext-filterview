An enhanced CKAN DataTables view that adds comparison operators (`=`, `!=`, `>`, `>=`, `<`, `<=`) and empty/non-empty checks to numeric and date columns — extending the official `datatablesview` plugin with client-side filtering for richer interactive data exploration.

![CKAN](https://img.shields.io/badge/ckan-%3E%3D2.10-orange.svg)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)

## Overview

`ckanext-filterview` is a drop-in replacement for the official `datatablesview` plugin. It keeps every feature of the upstream view and adds **range and comparison filtering** on numeric and date columns, which the original — limited to PostgreSQL full-text search — cannot do.

## Features

- Comparison operators on numeric and date/timestamp columns: `=`, `!=`, `>`, `>=`, `<`, `<=`
- Empty / not-empty filters
- Optional **client-side** filtering mode (configurable row limit, default 10,000) that powers the comparison operators
- **Server-side** mode preserved for large datasets (full-text search, exact match)
- Filtered export to CSV / JSON / XML
- All upstream features kept: sorting, pagination, column visibility, responsive layout, state saving, i18n (80+ languages)

## Requirements

| Software | Version |
| -------- | ------- |
| CKAN     | >= 2.10 |
| Python   | >= 3.8  |

## Installation

Activate your CKAN virtual environment, then:

```bash
pip install -e git+https://github.com/Wenze-Zhang/ckanext-filterview.git#egg=ckanext-filterview
```

Add `filterview` to `ckan.plugins` in your CKAN config (usually `/etc/ckan/default/ckan.ini`):

```ini
ckan.plugins = ... filterview
```

Restart CKAN.

## Usage

1. Open a resource that has data in the DataStore.
2. **Manage → Views → Add view → Table**.
3. Configure:
   - **Client Side Filtering** — enable to use comparison operators.
   - **Client Side Max Rows** — cap on rows loaded into the browser (default 10,000).

When client-side filtering is on, each numeric or date column gets an operator dropdown plus a value input:

| Column type | Examples |
| ----------- | -------- |
| Numeric     | `> 100`, `<= 50.5`, `between 10,100` |
| Date        | `> 2023-01-01`, `<= 2024-12-31` (use `yyyy-mm-dd`) |

For text columns, the input behaves as a case-insensitive substring match in client mode and as full-text search in server mode.

## Differences from the original `datatablesview`

| Feature             | `datatablesview`     | `ckanext-filterview` |
| ------------------- | -------------------- | -------------------- |
| Filtering mode      | Server-side only     | Server-side **or** client-side |
| Numeric filters     | Exact match          | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| Date filters        | Exact match          | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| Empty / non-empty   | —                    | ✓ |
| Max dataset size    | Unlimited            | Unlimited (server) / configurable (client) |

Use client-side mode for datasets under ~10,000 rows where comparison operators matter. Use server-side mode for very large datasets where simple text search is enough.

## Development

A Dockerised dev environment is bundled in [`dev/`](dev/):

```bash
git clone https://github.com/Wenze-Zhang/ckanext-filterview.git
cd ckanext-filterview/dev
cp .env.example .env
bin/compose build
bin/install_src
bin/compose up
```

On Windows, Docker must be integrated with WSL2.

## License

[AGPL-3.0-or-later](LICENSE). Based on the upstream [`ckanext-datatablesview`](https://github.com/ckan/ckanext-datatablesview).

## Credits

- Upstream: [ckanext-datatablesview](https://github.com/ckan/ckanext-datatablesview)
- [DataTables](https://datatables.net/) by SpryMedia Ltd
- [FontAwesome](https://fontawesome.com/) icons
- [DataTables i18n](https://datatables.net/plug-ins/i18n/) translations

## Support

Open an [issue](https://github.com/Wenze-Zhang/ckanext-filterview/issues) for bugs and feature requests. For CKAN itself, see the [CKAN documentation](https://docs.ckan.org/).

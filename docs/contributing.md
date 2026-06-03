# Contributing

## Development

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest
rhoso-api-docs-builder build --rhoso-version 18.0 --clean
rhoso-api-docs-builder validate --rhoso-version 18.0
```

## Updating Source Metadata

Keep updates small and citation-backed. If a Red Hat Docs page changes support
status or defaults, update `catalog.py`, regenerate `validation/` and `site/`,
and include the source URL in the change.

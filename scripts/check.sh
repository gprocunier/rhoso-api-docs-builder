#!/usr/bin/env bash
set -euo pipefail

ruff check .
pytest
rhoso-api-docs-builder build --rhoso-version 18.0 --clean
rhoso-api-docs-builder validate --rhoso-version 18.0
git diff --exit-code validation site

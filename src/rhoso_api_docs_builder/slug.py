from __future__ import annotations

import re


def slugify(value: str) -> str:
    """Create a stable lowercase path slug."""

    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def service_api_slug(service_name: str, project: str) -> str:
    display_name = service_name.split("(", 1)[0].strip()
    return slugify(f"{display_name}-{project}")

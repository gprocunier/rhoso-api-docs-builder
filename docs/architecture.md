# Architecture

The builder is a deterministic static generator.

```text
public source metadata -> normalized catalog -> manifest -> validation tree
                                      \-------> Red Hat-styled static site
```

## Components

- `catalog.py` contains citation-backed release, service, and API metadata.
- `models.py` defines the normalized release, service, API, and manifest types.
- `generator.py` intersects supported RHOSO services with upstream OpenStack API
  references and writes Markdown, JSON, and static HTML.
- `cli.py` exposes `releases`, `build`, and `validate`.

## Design Position

The generated HTML uses local CSS inspired by RHDS and PatternFly product-docs
principles: high contrast, restrained surfaces, clear tables/cards, strong focus
states, full-width use of browser real estate, and no external runtime assets.
The release page provides tile and list views. The generated output links to
RHDS as a source, but it does not require network-loaded design-system
components.

## Release Handling

RHOSO `18.0` is the only generated supported API release in v1. RHOSO `19.0` is
present in the root release picker as a beta mapping to OpenStack `2026.1`
`Gazpacho`, but the builder refuses to generate 19.0 API artifacts until public
Red Hat RHOSO 19 support data is added.

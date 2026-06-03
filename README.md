# RHOSO API Docs Builder

`rhoso-api-docs-builder` generates a Red Hat-styled validation tree for Red Hat
OpenStack Services on OpenShift (RHOSO) API documentation.

The tool answers two questions:

1. Which upstream OpenStack release maps to a selected RHOSO release?
2. Which upstream OpenStack API references belong to components Red Hat supports
   in that RHOSO release?

The first catalog supports RHOSO `18.0`, mapped to OpenStack `2023.1`
`Antelope`. RHOSO `19.0` is available in the site release picker as a beta
target mapped to OpenStack `2026.1` `Gazpacho`; generated RHOSO 19 API artifacts
are intentionally blocked until public Red Hat RHOSO 19 support documentation
exists.

## Install

```bash
python -m pip install -e '.[dev]'
```

The runtime path uses only the Python standard library. Development commands use
`pytest` and `ruff`.

## Build

```bash
rhoso-api-docs-builder releases
rhoso-api-docs-builder build --rhoso-version 18.0 --clean
rhoso-api-docs-builder validate --rhoso-version 18.0
```

Generated repository artifacts are written under:

```text
validation/<rhoso-version>/apis/<friendly-service-project>/
```

Generated static site artifacts are written under:

```text
site/validation/<rhoso-version>/
```

## URI Contract

For each supported API, the manifest emits all three URI forms:

- Semantic request URI:
  `https://github.com/gprocunier/rhoso-api-docs-builder/validation/<rhoso-version>/<friendly-tree>/...`
- Actual GitHub tree URI:
  `https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/<rhoso-version>/<friendly-tree>/...`
- GitHub Pages URI:
  `https://gprocunier.github.io/rhoso-api-docs-builder/validation/<rhoso-version>/<friendly-tree>/...`

## Source Policy

Red Hat Docs is the authority for which RHOSO services are supported. OpenStack
release docs are the authority for upstream API references in a mapped OpenStack
release. The generated output includes citations for both.

The API output does not expose service default deployment state. If Red Hat ships
the component in a supported state for the RHOSO release, it is included as a
supported API.

Primary sources for v1:

- Red Hat design system: https://ux.redhat.com/
- RHOSO 18.0 planning overview and service operators:
  https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/planning_your_deployment/assembly_red-hat-openstack-services-on-openshift-overview
- OpenStack 2023.1 API reference index:
  https://docs.openstack.org/2023.1/api/index.html
- OpenStack 2026.1 API reference index:
  https://docs.openstack.org/2026.1/api/index.html

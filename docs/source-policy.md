# Source Policy

The generator separates two source authorities.

Red Hat Docs decides whether a service is supported in RHOSO and provides the
primary API documentation link for the selected RHOSO release. The OpenStack API
reference index decides whether an API reference exists for the mapped upstream
OpenStack release and is retained as secondary upstream context.

Default deployment state is not part of the public API output. A Red
Hat-supported component is treated as supported; deployment enablement is a
separate operational concern.

## Priority

1. Public Red Hat Docs for RHOSO supported services, operators, limitations, and
   RHOSO-version-specific API documentation links.
2. Public OpenStack docs for mapped-release API reference coverage and upstream
   REST API details.
3. Versioned local overrides only when the public sources are ambiguous or
   missing. Overrides must include a reason and a citation.

## Unsupported And Unmatched Services

Some RHOSO-supported components are infrastructure services or UI components
without a matching upstream OpenStack API reference. These remain in
`supported-services.json` and are listed in the generated index as unmatched
services.

## RHOSO 19

RHOSO `19.0` is selectable as a beta target until public Red Hat documentation
identifies the supported RHOSO services for that release.

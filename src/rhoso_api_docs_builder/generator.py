from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from .catalog import (
    CATALOG_SNAPSHOT_DATE,
    DEFAULT_BRANCH,
    REPOSITORY,
    get_api_refs,
    get_release,
    get_services,
    list_releases,
    source_citations,
)
from .models import ReleaseMap, SupportedApi, SupportedService, ValidationManifest
from .slug import service_api_slug


def build_manifest(
    *,
    rhoso_version: str,
    repository: str = REPOSITORY,
    branch: str = DEFAULT_BRANCH,
    generated_at: str = CATALOG_SNAPSHOT_DATE,
) -> ValidationManifest:
    release = get_release(rhoso_version)
    services = get_services(rhoso_version)
    api_refs = get_api_refs(release.openstack_series)
    api_by_project = {api.project: api for api in api_refs}

    supported_apis: list[SupportedApi] = []
    unmatched_services: list[SupportedService] = []
    matched_projects: set[str] = set()

    for service in services:
        service_matched = False
        for project in service.api_projects:
            api_ref = api_by_project.get(project)
            if api_ref is None:
                continue
            slug = service_api_slug(service.name, project)
            relative = f"validation/{rhoso_version}/apis/{slug}/"
            supported_apis.append(
                SupportedApi(
                    service=service,
                    api_reference=api_ref,
                    slug=slug,
                    semantic_uri=f"https://github.com/{repository}/{relative}",
                    github_tree_uri=f"https://github.com/{repository}/tree/{branch}/{relative}",
                    pages_uri=(
                        f"https://{repository.split('/')[0]}.github.io/"
                        f"{repository.split('/')[1]}/validation/{rhoso_version}/apis/{slug}/"
                    ),
                )
            )
            matched_projects.add(project)
            service_matched = True
        if not service_matched:
            unmatched_services.append(service)

    selected_source_ids: list[str] = list(release.source_ids)
    for service in services:
        selected_source_ids.extend(service.source_ids)
    selected_source_ids.append(f"openstack-{release.openstack_series}-api")
    selected_source_ids.append("rhds-home")

    excluded = tuple(api for api in api_refs if api.project not in matched_projects)
    return ValidationManifest(
        generated_at=generated_at,
        catalog_snapshot_date=CATALOG_SNAPSHOT_DATE,
        repository=repository,
        branch=branch,
        release=release,
        sources=source_citations(selected_source_ids),
        supported_services=services,
        supported_apis=tuple(supported_apis),
        unmatched_supported_services=tuple(unmatched_services),
        excluded_upstream_apis=excluded,
    )


def build_outputs(
    *,
    rhoso_version: str,
    output: Path,
    site_output: Path | None,
    repository: str = REPOSITORY,
    branch: str = DEFAULT_BRANCH,
    generated_at: str = CATALOG_SNAPSHOT_DATE,
    clean: bool = False,
) -> ValidationManifest:
    manifest = build_manifest(
        rhoso_version=rhoso_version,
        repository=repository,
        branch=branch,
        generated_at=generated_at,
    )

    release_dir = output / rhoso_version
    if clean and release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)

    write_text(release_dir / "index.md", render_release_markdown(manifest))
    write_json(release_dir / "manifest.json", manifest.to_dict())
    write_json(
        release_dir / "supported-services.json",
        [service.to_dict() for service in manifest.supported_services],
    )

    for supported_api in manifest.supported_apis:
        api_dir = release_dir / "apis" / supported_api.slug
        api_dir.mkdir(parents=True, exist_ok=True)
        write_text(api_dir / "index.md", render_api_markdown(manifest, supported_api))
        write_json(api_dir / "metadata.json", supported_api.to_dict())

    if site_output is not None:
        build_site(manifest, site_output=site_output, clean=clean)

    return manifest


def validate_outputs(
    *,
    rhoso_version: str,
    output: Path,
    site_output: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    release_dir = output / rhoso_version
    manifest_path = release_dir / "manifest.json"
    if not manifest_path.exists():
        return [f"Missing manifest: {manifest_path}"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid manifest JSON: {exc}"]

    required_release_files = ["index.md", "supported-services.json"]
    for filename in required_release_files:
        path = release_dir / filename
        if not path.exists():
            errors.append(f"Missing release artifact: {path}")

    for item in manifest.get("supported_apis", []):
        slug = item.get("slug")
        if not slug:
            errors.append("Supported API entry without slug")
            continue
        api_dir = release_dir / "apis" / slug
        for filename in ("index.md", "metadata.json"):
            path = api_dir / filename
            if not path.exists():
                errors.append(f"Missing API artifact: {path}")
        metadata_path = api_dir / "metadata.json"
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata.get("slug") != slug:
                errors.append(f"Slug mismatch in {metadata_path}")

    if site_output is not None:
        site_index = site_output / "validation" / rhoso_version / "index.html"
        if not site_index.exists():
            errors.append(f"Missing site index: {site_index}")

    return errors


def write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_release_markdown(manifest: ValidationManifest) -> str:
    release = manifest.release
    api_rows = "\n".join(
        (
            f"| {api.service.name} | `{api.api_reference.project}` | "
            f"[{api.api_reference.service_label}]({api.api_reference.reference_url}) | "
            f"[tree]({api.github_tree_uri}) |"
        )
        for api in manifest.supported_apis
    )
    unmatched_rows = "\n".join(
        f"- {service.name} (`{service.operator}`): no upstream OpenStack API reference matched"
        for service in manifest.unmatched_supported_services
    )
    sources = "\n".join(
        f"- [{source.title}]({source.url}) - {source.note}" for source in manifest.sources
    )

    return f"""# RHOSO {release.rhoso_version} API validation

RHOSO {release.rhoso_version} maps to OpenStack {release.openstack_series}
{release.openstack_name}. This artifact intersects Red Hat-supported RHOSO
services with upstream OpenStack API references for that OpenStack release.

Generated at: `{manifest.generated_at}`

## Supported API Tree

| RHOSO service | OpenStack project | Upstream API | Repository artifact |
| --- | --- | --- | --- |
{api_rows}

## Supported Services Without A Matched OpenStack API Reference

{unmatched_rows}

## Sources

{sources}
"""


def render_api_markdown(manifest: ValidationManifest, api: SupportedApi) -> str:
    limitations = "\n".join(f"- {item}" for item in api.service.limitations) or "- None captured"
    guide = (
        f"\n- API guide: [{api.api_reference.guide_url}]({api.api_reference.guide_url})"
        if api.api_reference.guide_url
        else ""
    )
    return f"""# {api.service.name}

RHOSO version: `{manifest.release.rhoso_version}`
OpenStack release: `{manifest.release.openstack_series}` `{manifest.release.openstack_name}`
OpenStack project: `{api.api_reference.project}`
Operator: `{api.service.operator}`

## API Reference

- Reference: [{api.api_reference.reference_url}]({api.api_reference.reference_url}){guide}

## Validation URIs

- Semantic URI: `{api.semantic_uri}`
- GitHub tree URI: [{api.github_tree_uri}]({api.github_tree_uri})
- GitHub Pages URI: [{api.pages_uri}]({api.pages_uri})

## RHOSO Notes

{api.service.description}

## Captured Limitations

{limitations}
"""


def build_site(manifest: ValidationManifest, *, site_output: Path, clean: bool = False) -> None:
    if clean and site_output.exists():
        shutil.rmtree(site_output)
    (site_output / "validation" / manifest.release.rhoso_version / "apis").mkdir(
        parents=True, exist_ok=True
    )
    write_text(site_output / ".nojekyll", "")
    write_text(site_output / "index.html", render_site_home(manifest))
    write_text(site_output / "styles.css", render_css())
    release_dir = site_output / "validation" / manifest.release.rhoso_version
    write_text(release_dir / "index.html", render_release_html(manifest))
    for api in manifest.supported_apis:
        api_dir = release_dir / "apis" / api.slug
        api_dir.mkdir(parents=True, exist_ok=True)
        write_text(api_dir / "index.html", render_api_html(manifest, api))
    for release in list_releases():
        if release.rhoso_version == manifest.release.rhoso_version:
            continue
        release_page = site_output / "validation" / release.rhoso_version
        release_page.mkdir(parents=True, exist_ok=True)
        write_text(release_page / "index.html", render_unavailable_release_html(release))


def render_site_home(manifest: ValidationManifest) -> str:
    release_options = "\n".join(
        (
            f'        <option value="/rhoso-api-docs-builder/validation/{release.rhoso_version}/"'
            f"{' selected' if release.rhoso_version == manifest.release.rhoso_version else ''}>"
            f"RHOSO {html.escape(release.rhoso_version)}"
            f"{' beta' if release.status == 'beta' else ''}"
            f" - {html.escape(release.openstack_name)}</option>"
        )
        for release in list_releases()
    )
    return html_page(
        "RHOSO API Docs Builder",
        f"""
<section class="hero root-hero">
  <div>
    <p class="eyebrow">RHOSO API validation</p>
    <h1>Red Hat OpenStack Services on OpenShift API docs builder</h1>
    <p class="lead">Select an RHOSO release and inspect the Red Hat-supported OpenStack API
    references for that release.</p>
  </div>
  <form class="release-picker" action="/rhoso-api-docs-builder/validation/18.0/">
    <label for="release-select">Release</label>
    <select id="release-select" name="release"
      onchange="window.location.href = this.options[this.selectedIndex].value">
{release_options}
    </select>
    <a class="button" href="/rhoso-api-docs-builder/validation/{manifest.release.rhoso_version}/">
      Open RHOSO {html.escape(manifest.release.rhoso_version)}
    </a>
  </form>
</section>
<section class="metric-strip">
  <article>
    <span>{len(manifest.supported_apis)}</span>
    <p>supported API references</p>
  </article>
  <article>
    <span>{len(manifest.supported_services)}</span>
    <p>supported RHOSO services</p>
  </article>
  <article>
    <span>{len(list_releases())}</span>
    <p>tracked RHOSO releases</p>
  </article>
</section>
""",
    )


def render_release_html(manifest: ValidationManifest) -> str:
    api_cards = "\n".join(
        f"""
<article class="card">
  <p class="tag">Supported</p>
  <h2><a href="apis/{api.slug}/">{html.escape(api.service.name)}</a></h2>
  <p>{html.escape(api.service.description)}</p>
  <dl>
    <dt>Project</dt><dd>{html.escape(api.api_reference.project)}</dd>
    <dt>Operator</dt><dd>{html.escape(api.service.operator)}</dd>
  </dl>
</article>
"""
        for api in manifest.supported_apis
    )
    api_rows = "\n".join(
        f"""
<tr>
  <td data-label="RHOSO service"><a href="apis/{api.slug}/">{html.escape(api.service.name)}</a></td>
  <td data-label="OpenStack project"><code>{html.escape(api.api_reference.project)}</code></td>
  <td data-label="Operator">{html.escape(api.service.operator)}</td>
  <td data-label="Upstream API">
    <a href="{html.escape(api.api_reference.reference_url)}">API reference</a>
  </td>
</tr>
"""
        for api in manifest.supported_apis
    )
    unmatched = "\n".join(
        f"<li>{html.escape(service.name)} <code>{html.escape(service.operator)}</code></li>"
        for service in manifest.unmatched_supported_services
    )
    return html_page(
        f"RHOSO {manifest.release.rhoso_version} API validation",
        f"""
<section class="hero compact">
  <p class="eyebrow">OpenStack {html.escape(manifest.release.openstack_series)}
  {html.escape(manifest.release.openstack_name)}</p>
  <h1>RHOSO {html.escape(manifest.release.rhoso_version)} supported API tree</h1>
  <p class="lead">Every API listed here belongs to a component shipped in a supported state
  by Red Hat for this RHOSO release.</p>
</section>
<section class="view-controls" aria-label="View mode">
  <input type="radio" id="view-tiles" name="view-mode" checked>
  <label for="view-tiles">Tiles</label>
  <input type="radio" id="view-list" name="view-mode">
  <label for="view-list">List</label>
  <section class="grid api-tiles">{api_cards}</section>
  <section class="api-list">
    <table>
      <thead>
        <tr>
          <th>RHOSO service</th>
          <th>OpenStack project</th>
          <th>Operator</th>
          <th>Upstream API</th>
        </tr>
      </thead>
      <tbody>{api_rows}</tbody>
    </table>
  </section>
</section>
<section class="surface">
  <h2>Supported services without a matched OpenStack API reference</h2>
  <ul>{unmatched}</ul>
</section>
""",
    )


def render_unavailable_release_html(release: ReleaseMap) -> str:
    return html_page(
        f"RHOSO {release.rhoso_version} beta",
        f"""
<section class="hero compact">
  <p class="eyebrow">Beta release selection</p>
  <h1>RHOSO {html.escape(release.rhoso_version)} API tree</h1>
  <p class="lead">RHOSO {html.escape(release.rhoso_version)} is tracked as a beta target for
  OpenStack {html.escape(release.openstack_series)} {html.escape(release.openstack_name)}.
  Supported API output will be generated when public Red Hat support data is available.</p>
</section>
<section class="surface">
  <h2>Release mapping</h2>
  <dl>
    <dt>RHOSO</dt><dd>{html.escape(release.rhoso_version)}</dd>
    <dt>OpenStack</dt><dd>{html.escape(release.openstack_series)}
    {html.escape(release.openstack_name)}</dd>
    <dt>Status</dt><dd>Beta selection available, supported API data pending</dd>
  </dl>
</section>
""",
    )


def render_api_html(manifest: ValidationManifest, api: SupportedApi) -> str:
    limitations = "\n".join(f"<li>{html.escape(item)}</li>" for item in api.service.limitations)
    if not limitations:
        limitations = "<li>None captured</li>"
    reference_items = [
        (
            f'<li><a href="{html.escape(api.api_reference.reference_url)}">'
            "Upstream API reference</a></li>"
        )
    ]
    if api.api_reference.guide_url:
        reference_items.append(
            f'<li><a href="{html.escape(api.api_reference.guide_url)}">API guide</a></li>'
        )
    reference_list = "\n    ".join(reference_items)
    return html_page(
        api.service.name,
        f"""
<nav class="breadcrumb">
  <a href="../../">RHOSO {html.escape(manifest.release.rhoso_version)}</a>
</nav>
<section class="hero compact">
  <p class="eyebrow">{html.escape(api.api_reference.project)}</p>
  <h1>{html.escape(api.service.name)}</h1>
  <p class="lead">{html.escape(api.service.description)}</p>
</section>
<section class="surface">
  <h2>API reference</h2>
  <ul>
    {reference_list}
  </ul>
</section>
<section class="surface">
  <h2>Validation URIs</h2>
  <ul>
    <li><code>{html.escape(api.semantic_uri)}</code></li>
    <li><a href="{html.escape(api.github_tree_uri)}">GitHub tree artifact</a></li>
    <li><a href="{html.escape(api.pages_uri)}">GitHub Pages artifact</a></li>
  </ul>
</section>
<section class="surface">
  <h2>Captured limitations</h2>
  <ul>{limitations}</ul>
</section>
""",
    )


def html_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="/rhoso-api-docs-builder/styles.css">
</head>
<body>
  <header class="masthead">
    <a class="brand" href="/rhoso-api-docs-builder/">RHOSO API Docs Builder</a>
    <a href="https://ux.redhat.com/">RHDS</a>
    <a href="https://docs.redhat.com/">Red Hat Docs</a>
  </header>
  <main>{body}</main>
</body>
</html>
"""


def render_css() -> str:
    return """
:root {
  --rh-red: #ee0000;
  --rh-red-dark: #a60000;
  --ink: #151515;
  --muted: #4d4d4d;
  --border: #d2d2d2;
  --surface: #f5f5f5;
  --paper: #ffffff;
  --focus: #0066cc;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: "Red Hat Text", "Noto Sans", Arial, sans-serif;
  line-height: 1.5;
}
a { color: var(--rh-red-dark); }
a:focus { outline: 3px solid var(--focus); outline-offset: 3px; }
.masthead {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem clamp(1rem, 4vw, 3rem);
  border-bottom: 1px solid var(--border);
}
.brand {
  color: var(--ink);
  font-weight: 700;
  text-decoration: none;
  margin-right: auto;
}
main {
  width: 100%;
  margin: 0;
  padding: clamp(1rem, 3vw, 2.5rem);
}
.hero {
  background: var(--ink);
  color: white;
  padding: clamp(2rem, 6vw, 5rem);
  margin: 0 0 2rem;
}
.hero.compact { padding: clamp(1.5rem, 4vw, 3rem); }
.root-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 520px);
  gap: clamp(2rem, 6vw, 5rem);
  align-items: end;
}
.eyebrow {
  margin: 0 0 .75rem;
  color: #ffb3b3;
  font-weight: 700;
  text-transform: uppercase;
  font-size: .8rem;
}
h1 { margin: 0; font-size: 4rem; line-height: 1.05; max-width: 14ch; }
h2 { margin-top: 0; font-size: 1.2rem; }
.lead { max-width: 68ch; font-size: 1.15rem; }
.release-picker {
  display: grid;
  gap: .75rem;
  background: #ffffff;
  color: var(--ink);
  padding: 1.25rem;
  border: 1px solid var(--border);
  border-radius: 4px;
}
.release-picker label {
  color: var(--muted);
  font-weight: 700;
}
.release-picker select {
  width: 100%;
  min-height: 2.75rem;
  border: 1px solid var(--border);
  background: white;
  color: var(--ink);
  padding: 0 .75rem;
  font: inherit;
}
.button {
  display: inline-block;
  background: var(--rh-red);
  color: white;
  padding: .75rem 1rem;
  text-decoration: none;
  font-weight: 700;
  text-align: center;
}
.metric-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.metric-strip article {
  background: var(--surface);
  border-top: 4px solid var(--rh-red);
  padding: 1rem;
}
.metric-strip span {
  display: block;
  font-size: 4rem;
  font-weight: 700;
  line-height: 1;
}
.metric-strip p { margin: .5rem 0 0; color: var(--muted); }
.view-controls {
  display: block;
  margin-bottom: 1rem;
}
.view-controls > input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.view-controls > label {
  display: inline-block;
  min-width: 5.5rem;
  margin: 0 .35rem 1rem 0;
  padding: .55rem .8rem;
  border: 1px solid var(--border);
  background: var(--paper);
  color: var(--ink);
  text-align: center;
  font-weight: 700;
  cursor: pointer;
}
#view-tiles:checked + label,
#view-list:checked + label {
  background: var(--ink);
  border-color: var(--ink);
  color: white;
}
#view-list:checked ~ .api-tiles { display: none; }
#view-list:checked ~ .api-list { display: block; }
#view-tiles:checked ~ .api-list { display: none; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}
.card {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1rem;
  background: var(--paper);
}
.surface {
  background: var(--surface);
  border-top: 1px solid var(--border);
  margin-top: 1rem;
  padding: 1rem;
}
.api-list {
  overflow-x: auto;
  border: 1px solid var(--border);
  background: var(--paper);
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}
th, td {
  padding: .85rem 1rem;
  border-bottom: 1px solid var(--border);
  text-align: left;
  vertical-align: top;
}
th {
  background: var(--surface);
  font-size: .85rem;
  text-transform: uppercase;
}
.tag {
  display: inline-block;
  color: var(--rh-red-dark);
  font-weight: 700;
  margin: 0 0 .5rem;
}
dt { color: var(--muted); font-size: .85rem; }
dd { margin: 0 0 .5rem; font-weight: 700; }
code {
  background: #eeeeee;
  padding: .1rem .25rem;
  overflow-wrap: anywhere;
}
.breadcrumb { margin-bottom: 1rem; }
@media (max-width: 760px) {
  .masthead { align-items: flex-start; flex-direction: column; gap: .75rem; }
  .brand { margin-right: 0; }
  .root-hero { grid-template-columns: 1fr; }
  .metric-strip { grid-template-columns: 1fr; }
  h1 { font-size: 2.25rem; }
  .metric-strip span { font-size: 2.5rem; }
  table, thead, tbody, tr, th, td { display: block; }
  table { min-width: 0; }
  thead { display: none; }
  tr {
    border-bottom: 1px solid var(--border);
    padding: .75rem;
  }
  td {
    display: grid;
    grid-template-columns: 8.5rem minmax(0, 1fr);
    gap: .75rem;
    border-bottom: 0;
    padding: .35rem 0;
  }
  td::before {
    content: attr(data-label);
    color: var(--muted);
    font-weight: 700;
  }
}
"""

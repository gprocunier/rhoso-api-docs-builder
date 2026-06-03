import json
from pathlib import Path

from rhoso_api_docs_builder.generator import build_manifest, build_outputs, validate_outputs


def test_manifest_intersects_rhoso_services_with_openstack_api_refs() -> None:
    manifest = build_manifest(rhoso_version="18.0")
    projects = {api.api_reference.project for api in manifest.supported_apis}
    assert "nova" in projects
    assert "neutron" in projects
    assert "trove" not in projects
    assert any(service.name == "MariaDB" for service in manifest.unmatched_supported_services)


def test_build_outputs_writes_validation_tree(tmp_path: Path) -> None:
    output = tmp_path / "validation"
    site = tmp_path / "site"
    build_outputs(rhoso_version="18.0", output=output, site_output=site, clean=True)

    manifest_path = output / "18.0" / "manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["release"]["openstack_name"] == "Antelope"
    assert "default_state" not in json.dumps(manifest)
    for supported_api in manifest["supported_apis"]:
        api_reference = supported_api["api_reference"]
        assert (
            "docs.redhat.com/en/documentation/"
            "red_hat_openstack_services_on_openshift/18.0/"
            in api_reference["reference_url"]
        )
        upstream_reference_url = api_reference["upstream_reference_url"]
        assert upstream_reference_url.startswith("https://docs.openstack.org/")
        assert "/2023.1/" in upstream_reference_url
        assert upstream_reference_url != "https://docs.openstack.org/2023.1/api/index.html"
        assert "docs.openstack.org/api-ref" not in upstream_reference_url
        assert "/latest/" not in upstream_reference_url
        upstream_guide_url = api_reference["upstream_guide_url"]
        if upstream_guide_url:
            assert "/2023.1/" in upstream_guide_url
            assert "docs.openstack.org/api-guide" not in upstream_guide_url
            assert "/latest/" not in upstream_guide_url
    assert (output / "18.0" / "apis" / "compute-nova" / "index.md").exists()
    compute_html_path = site / "validation" / "18.0" / "apis" / "compute-nova" / "index.html"
    assert compute_html_path.exists()
    compute_html = compute_html_path.read_text(encoding="utf-8")
    assert "https://docs.openstack.org/nova/2023.1/#writing-to-the-api" in compute_html
    assert "https://docs.openstack.org/api-ref/compute/" not in compute_html
    baremetal_html = (
        site / "validation" / "18.0" / "apis" / "bare-metal-provisioning-ironic" / "index.html"
    ).read_text(encoding="utf-8")
    assert "https://docs.openstack.org/ironic/2023.1/contributor/webapi.html" in baremetal_html
    assert "https://docs.openstack.org/2023.1/api/index.html" not in baremetal_html
    assert (site / "validation" / "19.0" / "index.html").exists()


def test_site_includes_release_dropdown_and_tile_list_toggle(tmp_path: Path) -> None:
    site = tmp_path / "site"
    build_outputs(rhoso_version="18.0", output=tmp_path / "validation", site_output=site)
    home = (site / "index.html").read_text(encoding="utf-8")
    release = (site / "validation" / "18.0" / "index.html").read_text(encoding="utf-8")
    beta = (site / "validation" / "19.0" / "index.html").read_text(encoding="utf-8")
    assert "RHOSO 19.0 beta" in home
    assert 'id="view-tiles"' in release
    assert 'id="view-list"' in release
    assert "RHOSO API docs" in release
    assert "Beta selection available" in beta


def test_validate_outputs_reports_complete_tree(tmp_path: Path) -> None:
    output = tmp_path / "validation"
    site = tmp_path / "site"
    build_outputs(rhoso_version="18.0", output=output, site_output=site, clean=True)
    assert validate_outputs(rhoso_version="18.0", output=output, site_output=site) == []


def test_rhoso_19_build_is_blocked_until_red_hat_support_data_exists(tmp_path: Path) -> None:
    try:
        build_outputs(rhoso_version="19.0", output=tmp_path / "validation", site_output=None)
    except ValueError as exc:
        assert "does not have public supported-service data" in str(exc)
    else:
        raise AssertionError("RHOSO 19.0 generation should be blocked")

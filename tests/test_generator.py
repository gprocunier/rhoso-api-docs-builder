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
    assert (output / "18.0" / "apis" / "compute-nova" / "index.md").exists()
    assert (site / "validation" / "18.0" / "apis" / "compute-nova" / "index.html").exists()
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

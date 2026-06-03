from pathlib import Path

from rhoso_api_docs_builder.cli import main


def test_cli_releases_json(capsys) -> None:
    assert main(["releases", "--json"]) == 0
    captured = capsys.readouterr()
    assert '"rhoso_version": "18.0"' in captured.out
    assert '"openstack_name": "Gazpacho"' in captured.out


def test_cli_build_and_validate(tmp_path: Path, capsys) -> None:
    output = tmp_path / "validation"
    site = tmp_path / "site"
    assert (
        main(
            [
                "build",
                "--rhoso-version",
                "18.0",
                "--output",
                str(output),
                "--site-output",
                str(site),
                "--clean",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "validate",
                "--rhoso-version",
                "18.0",
                "--output",
                str(output),
                "--site-output",
                str(site),
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert "Generated RHOSO 18.0" in captured.out
    assert "Validation artifacts for RHOSO 18.0 are complete" in captured.out

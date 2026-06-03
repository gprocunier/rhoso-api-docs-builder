from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .catalog import CATALOG_SNAPSHOT_DATE, DEFAULT_BRANCH, REPOSITORY, list_releases
from .generator import build_outputs, validate_outputs


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rhoso-api-docs-builder",
        description="Build RHOSO API validation documentation.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    releases = subcommands.add_parser("releases", help="List known RHOSO release mappings")
    releases.add_argument("--json", action="store_true", help="Write machine-readable JSON")
    releases.set_defaults(func=cmd_releases)

    build = subcommands.add_parser("build", help="Generate validation artifacts")
    build.add_argument("--rhoso-version", required=True, help="RHOSO version, for example 18.0")
    build.add_argument(
        "--output", type=Path, default=Path("validation"), help="Validation output root"
    )
    build.add_argument(
        "--site-output", type=Path, default=Path("site"), help="GitHub Pages output root"
    )
    build.add_argument("--no-site", action="store_true", help="Skip static HTML site generation")
    build.add_argument("--repository", default=REPOSITORY, help="GitHub repository owner/name")
    build.add_argument("--branch", default=DEFAULT_BRANCH, help="Git branch for tree URIs")
    build.add_argument(
        "--generated-at",
        default=CATALOG_SNAPSHOT_DATE,
        help="Generation timestamp for deterministic builds",
    )
    build.add_argument(
        "--clean", action="store_true", help="Remove existing output for this release first"
    )
    build.set_defaults(func=cmd_build)

    validate = subcommands.add_parser("validate", help="Validate generated artifacts")
    validate.add_argument("--rhoso-version", required=True, help="RHOSO version, for example 18.0")
    validate.add_argument(
        "--output", type=Path, default=Path("validation"), help="Validation output root"
    )
    validate.add_argument(
        "--site-output", type=Path, default=Path("site"), help="GitHub Pages output root"
    )
    validate.add_argument("--no-site", action="store_true", help="Skip static site validation")
    validate.set_defaults(func=cmd_validate)

    return parser


def cmd_releases(args: argparse.Namespace) -> int:
    releases = [release.to_dict() for release in list_releases()]
    if args.json:
        print(json.dumps(releases, indent=2, sort_keys=True))
        return 0

    print("RHOSO  OpenStack  Name       Status")
    print("-----  ---------  ---------  ---------")
    for release in list_releases():
        print(
            f"{release.rhoso_version:<5}  {release.openstack_series:<9}  "
            f"{release.openstack_name:<9}  {release.status}"
        )
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    site_output = None if args.no_site else args.site_output
    manifest = build_outputs(
        rhoso_version=args.rhoso_version,
        output=args.output,
        site_output=site_output,
        repository=args.repository,
        branch=args.branch,
        generated_at=args.generated_at,
        clean=args.clean,
    )
    print(
        f"Generated RHOSO {manifest.release.rhoso_version}: "
        f"{len(manifest.supported_apis)} API artifacts, "
        f"{len(manifest.supported_services)} services"
    )
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    site_output = None if args.no_site else args.site_output
    errors = validate_outputs(
        rhoso_version=args.rhoso_version,
        output=args.output,
        site_output=site_output,
    )
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Validation artifacts for RHOSO {args.rhoso_version} are complete")
    return 0

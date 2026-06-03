from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class SourceCitation:
    """A public source used to justify release or service metadata."""

    id: str
    title: str
    url: str
    note: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseMap:
    rhoso_version: str
    openstack_series: str
    openstack_name: str
    status: str
    source_ids: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ApiReference:
    project: str
    service_label: str
    reference_url: str
    guide_url: str | None = None
    upstream_reference_url: str | None = None
    upstream_guide_url: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class SupportedService:
    name: str
    operator: str
    description: str
    support_status: str
    api_projects: tuple[str, ...]
    source_ids: tuple[str, ...]
    limitations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class SupportedApi:
    service: SupportedService
    api_reference: ApiReference
    slug: str
    semantic_uri: str
    github_tree_uri: str
    pages_uri: str

    def to_dict(self) -> dict[str, object]:
        return {
            "slug": self.slug,
            "service": self.service.to_dict(),
            "api_reference": self.api_reference.to_dict(),
            "uris": {
                "semantic": self.semantic_uri,
                "github_tree": self.github_tree_uri,
                "pages": self.pages_uri,
            },
        }


@dataclass(frozen=True)
class ValidationManifest:
    generated_at: str
    catalog_snapshot_date: str
    repository: str
    branch: str
    release: ReleaseMap
    sources: tuple[SourceCitation, ...]
    supported_services: tuple[SupportedService, ...]
    supported_apis: tuple[SupportedApi, ...]
    unmatched_supported_services: tuple[SupportedService, ...] = field(default_factory=tuple)
    excluded_upstream_apis: tuple[ApiReference, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "generated_at": self.generated_at,
            "catalog_snapshot_date": self.catalog_snapshot_date,
            "repository": self.repository,
            "branch": self.branch,
            "release": self.release.to_dict(),
            "sources": [source.to_dict() for source in self.sources],
            "supported_services": [service.to_dict() for service in self.supported_services],
            "supported_apis": [api.to_dict() for api in self.supported_apis],
            "unmatched_supported_services": [
                service.to_dict() for service in self.unmatched_supported_services
            ],
            "excluded_upstream_apis": [api.to_dict() for api in self.excluded_upstream_apis],
        }

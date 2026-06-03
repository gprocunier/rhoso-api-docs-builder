from __future__ import annotations

from collections.abc import Iterable

from .models import ApiReference, ReleaseMap, SourceCitation, SupportedService

CATALOG_SNAPSHOT_DATE = "2026-06-03"

REPOSITORY = "gprocunier/rhoso-api-docs-builder"
DEFAULT_BRANCH = "main"
OPENSTACK_2023_1_API_INDEX = "https://docs.openstack.org/2023.1/api/index.html"
OPENSTACK_2026_1_API_INDEX = "https://docs.openstack.org/2026.1/api/index.html"
OPENSTACK_2023_1_PROJECT_DOCS = "https://docs.openstack.org/{project}/2023.1/{path}"
OPENSTACK_2026_1_PROJECT_DOCS = "https://docs.openstack.org/{project}/2026.1/{path}"


def openstack_2023_1_project_url(project: str, path: str = "") -> str:
    return OPENSTACK_2023_1_PROJECT_DOCS.format(project=project, path=path)


def openstack_2026_1_project_url(project: str, path: str = "") -> str:
    return OPENSTACK_2026_1_PROJECT_DOCS.format(project=project, path=path)

SOURCES: dict[str, SourceCitation] = {
    "rhds-home": SourceCitation(
        id="rhds-home",
        title="Red Hat design system",
        url="https://ux.redhat.com/",
        note=(
            "Design language, elements, tokens, and accessibility guidance for "
            "Red Hat digital experiences."
        ),
    ),
    "rhoso-18-overview": SourceCitation(
        id="rhoso-18-overview",
        title="RHOSO 18.0 planning overview and service operators",
        url=(
            "https://docs.redhat.com/en/documentation/"
            "red_hat_openstack_services_on_openshift/18.0/html/"
            "planning_your_deployment/"
            "assembly_red-hat-openstack-services-on-openshift-overview"
        ),
        note="Primary RHOSO 18.0 source for service operators and known limitations.",
    ),
    "rhoso-18-docs": SourceCitation(
        id="rhoso-18-docs",
        title="RHOSO 18.0 Red Hat documentation index",
        url="https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0",
        note="Version-specific Red Hat documentation used for primary API documentation links.",
    ),
    "openstack-2023.1-api": SourceCitation(
        id="openstack-2023.1-api",
        title="OpenStack 2023.1 API reference index",
        url=OPENSTACK_2023_1_API_INDEX,
        note="Upstream API references for OpenStack 2023.1 Antelope.",
    ),
    "openstack-2026.1-api": SourceCitation(
        id="openstack-2026.1-api",
        title="OpenStack 2026.1 API reference index",
        url=OPENSTACK_2026_1_API_INDEX,
        note="Upstream API references for OpenStack 2026.1 Gazpacho.",
    ),
    "openstack-gazpacho": SourceCitation(
        id="openstack-gazpacho",
        title="OpenStack Gazpacho release information",
        url="https://www.openstack.org/software/openstack-gazpacho",
        note="Release identity for OpenStack 2026.1 Gazpacho.",
    ),
}

RHOSO_18_DOC_BASE = (
    "https://docs.redhat.com/en/documentation/"
    "red_hat_openstack_services_on_openshift/18.0/html"
)

RHOSO_API_DOC_URLS: dict[str, dict[str, str]] = {
    "18.0": {
        "barbican": f"{RHOSO_18_DOC_BASE}/configuring_security_services/index",
        "cinder": f"{RHOSO_18_DOC_BASE}/performing_storage_operations/index",
        "designate": f"{RHOSO_18_DOC_BASE}/configuring_dns_as_a_service/index",
        "glance": f"{RHOSO_18_DOC_BASE}/performing_storage_operations/index",
        "heat": f"{RHOSO_18_DOC_BASE}/autoscaling_for_instances/index",
        "ironic": f"{RHOSO_18_DOC_BASE}/configuring_the_bare_metal_provisioning_service/index",
        "keystone": f"{RHOSO_18_DOC_BASE}/configuring_security_services/index",
        "manila": f"{RHOSO_18_DOC_BASE}/performing_storage_operations/index",
        "neutron": f"{RHOSO_18_DOC_BASE}/configuring_networking_services/index",
        "nova": f"{RHOSO_18_DOC_BASE}/configuring_the_compute_service_for_instance_creation/index",
        "octavia": f"{RHOSO_18_DOC_BASE}/configuring_load_balancing_as_a_service/index",
        "placement": f"{RHOSO_18_DOC_BASE}/configuration_reference/placement_3",
        "swift": f"{RHOSO_18_DOC_BASE}/performing_storage_operations/index",
    },
}

RELEASES: dict[str, ReleaseMap] = {
    "18.0": ReleaseMap(
        rhoso_version="18.0",
        openstack_series="2023.1",
        openstack_name="Antelope",
        status="supported",
        source_ids=("rhoso-18-overview", "rhoso-18-docs", "openstack-2023.1-api"),
        notes=(
            "RHOSO 18.0 is mapped to OpenStack 2023.1 Antelope for this tool's v1 catalog.",
        ),
    ),
    "19.0": ReleaseMap(
        rhoso_version="19.0",
        openstack_series="2026.1",
        openstack_name="Gazpacho",
        status="beta",
        source_ids=("openstack-2026.1-api", "openstack-gazpacho"),
        notes=(
            "RHOSO 19.0 support data is intentionally not generated until public Red Hat "
            "RHOSO 19 docs identify supported services.",
        ),
    ),
}

OPENSTACK_API_REFS: dict[str, tuple[ApiReference, ...]] = {
    "2023.1": (
        ApiReference(
            "cyborg",
            "Accelerator Life Cycle Management",
            openstack_2023_1_project_url("cyborg"),
        ),
        ApiReference("murano", "Application Catalog", openstack_2023_1_project_url("murano")),
        ApiReference(
            "freezer",
            "Backup, Restore, and Disaster Recovery",
            openstack_2023_1_project_url("freezer"),
        ),
        ApiReference(
            "ironic",
            "Bare Metal",
            openstack_2023_1_project_url("ironic", "contributor/webapi.html"),
            openstack_2023_1_project_url("ironic", "contributor/webapi-version-history.html"),
        ),
        ApiReference(
            "cinder",
            "Block Storage",
            openstack_2023_1_project_url("cinder", "#using-the-cinder-api"),
            openstack_2023_1_project_url("cinder", "contributor/api_microversion_history.html"),
        ),
        ApiReference("senlin", "Clustering", openstack_2023_1_project_url("senlin")),
        ApiReference(
            "nova",
            "Compute",
            openstack_2023_1_project_url("nova", "#writing-to-the-api"),
            openstack_2023_1_project_url("nova", "reference/api-microversion-history.html"),
        ),
        ApiReference(
            "magnum",
            "Container Infrastructure Management",
            openstack_2023_1_project_url("magnum"),
        ),
        ApiReference("zun", "Containers", openstack_2023_1_project_url("zun")),
        ApiReference("trove", "Database", openstack_2023_1_project_url("trove")),
        ApiReference(
            "designate",
            "DNS",
            openstack_2023_1_project_url("designate", "contributor/sourcedoc/api.html"),
        ),
        ApiReference(
            "ec2-api",
            "EC2 API compatibility layer",
            openstack_2023_1_project_url("ec2-api"),
        ),
        ApiReference(
            "keystone",
            "Identity",
            openstack_2023_1_project_url("keystone", "contributor/http-api.html"),
            openstack_2023_1_project_url("keystone", "api_curl_examples.html"),
        ),
        ApiReference(
            "glance",
            "Image",
            openstack_2023_1_project_url("glance", "contributor/api/glance.api.v2.html"),
        ),
        ApiReference(
            "watcher",
            "Infrastructure Optimization",
            openstack_2023_1_project_url("watcher"),
        ),
        ApiReference(
            "masakari",
            "Instances High Availability",
            openstack_2023_1_project_url("masakari"),
        ),
        ApiReference("barbican", "Key Manager", "https://docs.openstack.org/barbican/2023.1/api/"),
        ApiReference(
            "octavia",
            "Load-balancer",
            openstack_2023_1_project_url(
                "octavia",
                "contributor/modules/octavia.api.v2.html",
            ),
        ),
        ApiReference("venus", "Log Management", openstack_2023_1_project_url("venus")),
        ApiReference("zaqar", "Messaging", openstack_2023_1_project_url("zaqar")),
        ApiReference(
            "neutron",
            "Networking",
            openstack_2023_1_project_url("neutron", "#api-reference"),
        ),
        ApiReference(
            "tacker",
            "NFV Orchestration",
            openstack_2023_1_project_url("tacker"),
        ),
        ApiReference(
            "swift",
            "Object Storage",
            openstack_2023_1_project_url("swift", "api/object_api_v1_overview.html"),
        ),
        ApiReference(
            "heat",
            "Orchestration",
            "https://docs.openstack.org/heat/2023.1/api/",
            "https://docs.openstack.org/heat/2023.1/template_guide/",
        ),
        ApiReference(
            "placement",
            "Placement",
            openstack_2023_1_project_url("placement", "user/index.html#rest-api"),
            openstack_2023_1_project_url(
                "placement",
                "placement-api-microversion-history.html",
            ),
        ),
        ApiReference("cloudkitty", "Rating", openstack_2023_1_project_url("cloudkitty")),
        ApiReference("blazar", "Resource reservation", openstack_2023_1_project_url("blazar")),
        ApiReference(
            "manila",
            "Shared File Systems",
            openstack_2023_1_project_url("manila", "#using-the-manila-api"),
            openstack_2023_1_project_url("manila", "contributor/api_microversion_history.html"),
        ),
    ),
    "2026.1": (
        ApiReference(
            "cyborg",
            "Accelerator Life Cycle Management",
            openstack_2026_1_project_url("cyborg"),
        ),
        ApiReference(
            "ironic",
            "Bare Metal",
            openstack_2026_1_project_url("ironic", "contributor/webapi.html"),
            openstack_2026_1_project_url("ironic", "contributor/webapi-version-history.html"),
        ),
        ApiReference(
            "cinder",
            "Block Storage",
            openstack_2026_1_project_url("cinder", "#using-the-cinder-api"),
            openstack_2026_1_project_url("cinder", "contributor/api_microversion_history.html"),
        ),
        ApiReference(
            "nova",
            "Compute",
            openstack_2026_1_project_url("nova", "#writing-to-the-api"),
            openstack_2026_1_project_url("nova", "reference/api-microversion-history.html"),
        ),
        ApiReference(
            "magnum",
            "Container Infrastructure Management",
            openstack_2026_1_project_url("magnum"),
        ),
        ApiReference("trove", "Database", openstack_2026_1_project_url("trove")),
        ApiReference(
            "designate",
            "DNS",
            openstack_2026_1_project_url("designate", "contributor/sourcedoc/api.html"),
        ),
        ApiReference(
            "keystone",
            "Identity",
            openstack_2026_1_project_url("keystone", "contributor/http-api.html"),
            openstack_2026_1_project_url("keystone", "api_curl_examples.html"),
        ),
        ApiReference(
            "glance",
            "Image",
            openstack_2026_1_project_url("glance", "contributor/api/glance.api.v2.html"),
        ),
        ApiReference(
            "watcher",
            "Infrastructure Optimization",
            openstack_2026_1_project_url("watcher"),
        ),
        ApiReference(
            "masakari",
            "Instances High Availability",
            openstack_2026_1_project_url("masakari"),
        ),
        ApiReference("barbican", "Key Manager", "https://docs.openstack.org/barbican/2026.1/api/"),
        ApiReference(
            "octavia",
            "Load-balancer",
            openstack_2026_1_project_url(
                "octavia",
                "contributor/modules/octavia.api.v2.html",
            ),
        ),
        ApiReference("zaqar", "Messaging", openstack_2026_1_project_url("zaqar")),
        ApiReference(
            "neutron",
            "Networking",
            openstack_2026_1_project_url("neutron", "#api-reference"),
        ),
        ApiReference(
            "swift",
            "Object Storage",
            openstack_2026_1_project_url("swift", "api/object_api_v1_overview.html"),
        ),
        ApiReference(
            "heat",
            "Orchestration",
            "https://docs.openstack.org/heat/2026.1/api/",
            "https://docs.openstack.org/heat/2026.1/template_guide/",
        ),
        ApiReference(
            "placement",
            "Placement",
            openstack_2026_1_project_url("placement", "user/index.html#rest-api"),
            openstack_2026_1_project_url(
                "placement",
                "placement-api-microversion-history.html",
            ),
        ),
        ApiReference("cloudkitty", "Rating", openstack_2026_1_project_url("cloudkitty")),
        ApiReference("blazar", "Resource reservation", openstack_2026_1_project_url("blazar")),
        ApiReference(
            "manila",
            "Shared File Systems",
            openstack_2026_1_project_url("manila", "#using-the-manila-api"),
            openstack_2026_1_project_url("manila", "contributor/api_microversion_history.html"),
        ),
    ),
}

RHOSO_SERVICES: dict[str, tuple[SupportedService, ...]] = {
    "18.0": (
        SupportedService(
            "Bare Metal Provisioning (ironic)",
            "ironic-operator",
            "Supports physical machines with hardware-specific drivers and integrates with "
            "Compute.",
            "supported",
            ("ironic",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "OpenStack bare-metal provisioning operator",
            "openstack-baremetal-operator",
            "Used by the OpenStack Operator during bare-metal node provisioning.",
            "supported",
            (),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Block Storage (cinder)",
            "cinder-operator",
            "Provides and manages persistent block storage volumes for virtual machine instances.",
            "supported",
            ("cinder",),
            ("rhoso-18-overview",),
            ("Cinder replication", "LVM driver", "NFS versions earlier than 4"),
        ),
        SupportedService(
            "Compute (nova)",
            "nova-operator",
            "Provides compute resource provisioning through libvirt or ironic drivers.",
            "supported",
            ("nova",),
            ("rhoso-18-overview",),
            (
                "Off-path network backends",
                "Custom policies without support exception",
                "nova-serialproxy and nova-spicehtml5proxy packages",
                "File injection of personality files",
                "Persistent memory for instances",
                "QEMU emulation of non-native architectures",
                "LVM as an image backend",
                "ploop image format",
                "NFS versions earlier than 4",
            ),
        ),
        SupportedService(
            "Dashboard (horizon)",
            "horizon-operator",
            "Provides a browser-based dashboard for cloud resources and user access.",
            "supported",
            (),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "DNS (designate)",
            "designate-operator",
            "Provides DNS as a service and a REST API integrated with Networking and Identity.",
            "supported",
            ("designate",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Identity (keystone)",
            "keystone-operator",
            "Provides authentication, authorization, users, projects, and roles.",
            "supported",
            ("keystone",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Image (glance)",
            "glance-operator",
            "Stores virtual machine images and volume snapshots.",
            "supported",
            ("glance",),
            ("rhoso-18-overview",),
            ("Only x86_64 architecture is supported", "NFS versions earlier than 4"),
        ),
        SupportedService(
            "Key Management (barbican)",
            "barbican-operator",
            "Provides secure storage and management of secrets, keys, and certificates.",
            "supported",
            ("barbican",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Load balancing (octavia)",
            "octavia-operator",
            "Provides load balancing as a service for cloud workloads.",
            "supported",
            ("octavia",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "MariaDB",
            "mariadb-operator",
            "Deploys and manages MariaDB Galera clusters for RHOSO infrastructure.",
            "supported",
            (),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Memcached",
            "infra-operator",
            "Provides infrastructure caching support.",
            "supported",
            (),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Networking (neutron)",
            "neutron-operator",
            "Provides networking as a service for virtual compute environments.",
            "supported",
            ("neutron",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Object Storage (swift)",
            "swift-operator",
            "Provides durable object storage for unstructured data.",
            "supported",
            ("swift",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "OVN",
            "ovn-operator",
            "Deploys and manages OVN infrastructure.",
            "supported",
            (),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Orchestration (heat)",
            "heat-operator",
            "Provides template-based orchestration of cloud resource stacks.",
            "supported",
            ("heat",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Placement (placement)",
            "placement-operator",
            "Installs and manages OpenStack Placement.",
            "supported",
            ("placement",),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "RabbitMQ",
            "rabbitmq-cluster-operator",
            "Deploys and manages RabbitMQ clusters for RHOSO infrastructure.",
            "supported",
            (),
            ("rhoso-18-overview",),
        ),
        SupportedService(
            "Shared File Systems (manila)",
            "manila-operator",
            "Provisions shared file systems for virtual machines, bare-metal nodes, and "
            "containers.",
            "supported",
            ("manila",),
            ("rhoso-18-overview",),
            ("NFS versions earlier than 4.1 for CephFS-NFS back ends",),
        ),
        SupportedService(
            "Telemetry (ceilometer, prometheus)",
            "telemetry-operator",
            "Collects usage data for billing, monitoring, and alerts.",
            "supported",
            ("ceilometer", "prometheus"),
            ("rhoso-18-overview",),
        ),
    ),
}


def catalog_snapshot_date() -> str:
    return CATALOG_SNAPSHOT_DATE


def list_releases() -> tuple[ReleaseMap, ...]:
    return tuple(RELEASES.values())


def get_release(rhoso_version: str) -> ReleaseMap:
    try:
        return RELEASES[rhoso_version]
    except KeyError as exc:
        supported = ", ".join(sorted(RELEASES))
        raise KeyError(
            f"Unsupported RHOSO version {rhoso_version!r}; known versions: {supported}"
        ) from exc


def get_services(rhoso_version: str) -> tuple[SupportedService, ...]:
    services = RHOSO_SERVICES.get(rhoso_version)
    if not services:
        raise ValueError(
            f"RHOSO {rhoso_version} does not have public supported-service data in this catalog."
        )
    return services


def get_api_refs(openstack_series: str) -> tuple[ApiReference, ...]:
    try:
        return OPENSTACK_API_REFS[openstack_series]
    except KeyError as exc:
        supported = ", ".join(sorted(OPENSTACK_API_REFS))
        raise KeyError(
            f"Unsupported OpenStack series {openstack_series!r}; known series: {supported}"
        ) from exc


def get_rhoso_api_doc_url(rhoso_version: str, project: str) -> str:
    try:
        return RHOSO_API_DOC_URLS[rhoso_version][project]
    except KeyError as exc:
        raise KeyError(
            f"No RHOSO {rhoso_version} API documentation URL is mapped for {project!r}"
        ) from exc


def source_citations(source_ids: Iterable[str]) -> tuple[SourceCitation, ...]:
    seen: set[str] = set()
    sources: list[SourceCitation] = []
    for source_id in source_ids:
        if source_id not in seen:
            sources.append(SOURCES[source_id])
            seen.add(source_id)
    return tuple(sources)

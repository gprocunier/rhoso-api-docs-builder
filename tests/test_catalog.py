from rhoso_api_docs_builder.catalog import (
    get_api_refs,
    get_release,
    get_rhoso_api_doc_url,
    get_services,
)


def test_rhoso_18_release_mapping() -> None:
    release = get_release("18.0")
    assert release.openstack_series == "2023.1"
    assert release.openstack_name == "Antelope"
    assert release.status == "supported"


def test_rhoso_19_is_beta_placeholder() -> None:
    release = get_release("19.0")
    assert release.openstack_series == "2026.1"
    assert release.openstack_name == "Gazpacho"
    assert release.status == "beta"


def test_supported_services_do_not_expose_deployment_defaults() -> None:
    services = get_services("18.0")
    assert all(not hasattr(service, "default_state") for service in services)
    assert {service.support_status for service in services} == {"supported"}


def test_single_item_limitations_are_tuples_not_character_sequences() -> None:
    services = {service.name: service for service in get_services("18.0")}
    manila = services["Shared File Systems (manila)"]
    assert manila.limitations == ("NFS versions earlier than 4.1 for CephFS-NFS back ends",)


def test_openstack_api_refs_include_core_supported_projects() -> None:
    refs = {api.project for api in get_api_refs("2023.1")}
    assert {"nova", "neutron", "cinder", "keystone", "glance", "manila"} <= refs


def test_rhoso_api_doc_urls_are_release_specific() -> None:
    assert (
        get_rhoso_api_doc_url("18.0", "nova")
        == "https://docs.redhat.com/en/documentation/"
        "red_hat_openstack_services_on_openshift/18.0/html/"
        "configuring_the_compute_service_for_instance_creation/index"
    )

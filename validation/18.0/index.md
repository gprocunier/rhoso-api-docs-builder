# RHOSO 18.0 API validation

RHOSO 18.0 maps to OpenStack 2023.1
Antelope. This artifact intersects Red Hat-supported RHOSO
services with OpenStack API references, and links each matched API to the
version-specific RHOSO documentation for this release.

Generated at: `2026-06-03`

## Supported API Tree

| RHOSO service | OpenStack project | RHOSO API docs | Repository artifact |
| --- | --- | --- | --- |
| Bare Metal Provisioning (ironic) | `ironic` | [Bare Metal](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_the_bare_metal_provisioning_service/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/bare-metal-provisioning-ironic/) |
| Block Storage (cinder) | `cinder` | [Block Storage](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/performing_storage_operations/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/block-storage-cinder/) |
| Compute (nova) | `nova` | [Compute](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_the_compute_service_for_instance_creation/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/compute-nova/) |
| DNS (designate) | `designate` | [DNS](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_dns_as_a_service/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/dns-designate/) |
| Identity (keystone) | `keystone` | [Identity](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_security_services/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/identity-keystone/) |
| Image (glance) | `glance` | [Image](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/performing_storage_operations/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/image-glance/) |
| Key Management (barbican) | `barbican` | [Key Manager](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_security_services/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/key-management-barbican/) |
| Load balancing (octavia) | `octavia` | [Load-balancer](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_load_balancing_as_a_service/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/load-balancing-octavia/) |
| Networking (neutron) | `neutron` | [Networking](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_networking_services/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/networking-neutron/) |
| Object Storage (swift) | `swift` | [Object Storage](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/performing_storage_operations/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/object-storage-swift/) |
| Orchestration (heat) | `heat` | [Orchestration](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/autoscaling_for_instances/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/orchestration-heat/) |
| Placement (placement) | `placement` | [Placement](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuration_reference/placement_3) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/placement-placement/) |
| Shared File Systems (manila) | `manila` | [Shared File Systems](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/performing_storage_operations/index) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/shared-file-systems-manila/) |

## Supported Services Without A Matched OpenStack API Reference

- OpenStack bare-metal provisioning operator (`openstack-baremetal-operator`): no upstream OpenStack API reference matched
- Dashboard (horizon) (`horizon-operator`): no upstream OpenStack API reference matched
- MariaDB (`mariadb-operator`): no upstream OpenStack API reference matched
- Memcached (`infra-operator`): no upstream OpenStack API reference matched
- OVN (`ovn-operator`): no upstream OpenStack API reference matched
- RabbitMQ (`rabbitmq-cluster-operator`): no upstream OpenStack API reference matched
- Telemetry (ceilometer, prometheus) (`telemetry-operator`): no upstream OpenStack API reference matched

## Sources

- [RHOSO 18.0 planning overview and service operators](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/planning_your_deployment/assembly_red-hat-openstack-services-on-openshift-overview) - Primary RHOSO 18.0 source for service operators and known limitations.
- [RHOSO 18.0 Red Hat documentation index](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0) - Version-specific Red Hat documentation used for primary API documentation links.
- [OpenStack 2023.1 API reference index](https://docs.openstack.org/2023.1/api/index.html) - Upstream API references for OpenStack 2023.1 Antelope.
- [Red Hat design system](https://ux.redhat.com/) - Design language, elements, tokens, and accessibility guidance for Red Hat digital experiences.

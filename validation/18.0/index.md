# RHOSO 18.0 API validation

RHOSO 18.0 maps to OpenStack 2023.1
Antelope. This artifact intersects Red Hat-supported RHOSO
services with upstream OpenStack API references for that OpenStack release.

Generated at: `2026-06-03`

## Supported API Tree

| RHOSO service | OpenStack project | Upstream API | Repository artifact |
| --- | --- | --- | --- |
| Bare Metal Provisioning (ironic) | `ironic` | [Bare Metal](https://docs.openstack.org/api-ref/baremetal/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/bare-metal-provisioning-ironic/) |
| Block Storage (cinder) | `cinder` | [Block Storage](https://docs.openstack.org/api-ref/block-storage/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/block-storage-cinder/) |
| Compute (nova) | `nova` | [Compute](https://docs.openstack.org/api-ref/compute/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/compute-nova/) |
| DNS (designate) | `designate` | [DNS](https://docs.openstack.org/api-ref/dns/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/dns-designate/) |
| Identity (keystone) | `keystone` | [Identity](https://docs.openstack.org/api-ref/identity/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/identity-keystone/) |
| Image (glance) | `glance` | [Image](https://docs.openstack.org/api-ref/image/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/image-glance/) |
| Key Management (barbican) | `barbican` | [Key Manager](https://docs.openstack.org/barbican/2023.1/api/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/key-management-barbican/) |
| Load balancing (octavia) | `octavia` | [Load-balancer](https://docs.openstack.org/api-ref/load-balancer/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/load-balancing-octavia/) |
| Networking (neutron) | `neutron` | [Networking](https://docs.openstack.org/api-ref/network/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/networking-neutron/) |
| Object Storage (swift) | `swift` | [Object Storage](https://docs.openstack.org/api-ref/object-store/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/object-storage-swift/) |
| Orchestration (heat) | `heat` | [Orchestration](https://docs.openstack.org/api-ref/orchestration/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/orchestration-heat/) |
| Placement (placement) | `placement` | [Placement](https://docs.openstack.org/api-ref/placement/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/placement-placement/) |
| Shared File Systems (manila) | `manila` | [Shared File Systems](https://docs.openstack.org/api-ref/shared-file-system/) | [tree](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/shared-file-systems-manila/) |

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
- [OpenStack 2023.1 API reference index](https://docs.openstack.org/2023.1/api/index.html) - Upstream API references for OpenStack 2023.1 Antelope.
- [Red Hat design system](https://ux.redhat.com/) - Design language, elements, tokens, and accessibility guidance for Red Hat digital experiences.

# Shared File Systems (manila)

RHOSO version: `18.0`
OpenStack release: `2023.1` `Antelope`
OpenStack project: `manila`
Operator: `manila-operator`

## API Reference

- RHOSO 18.0 docs: [https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/performing_storage_operations/index](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/performing_storage_operations/index)
- OpenStack API reference: [https://docs.openstack.org/manila/2023.1/#using-the-manila-api](https://docs.openstack.org/manila/2023.1/#using-the-manila-api)
- OpenStack API guide: [https://docs.openstack.org/manila/2023.1/contributor/api_microversion_history.html](https://docs.openstack.org/manila/2023.1/contributor/api_microversion_history.html)

## Validation URIs

- Semantic URI: `https://github.com/gprocunier/rhoso-api-docs-builder/validation/18.0/apis/shared-file-systems-manila/`
- GitHub tree URI: [https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/shared-file-systems-manila/](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/shared-file-systems-manila/)
- GitHub Pages URI: [https://gprocunier.github.io/rhoso-api-docs-builder/validation/18.0/apis/shared-file-systems-manila/](https://gprocunier.github.io/rhoso-api-docs-builder/validation/18.0/apis/shared-file-systems-manila/)

## RHOSO Notes

Provisions shared file systems for virtual machines, bare-metal nodes, and containers.

## Captured Limitations

- NFS versions earlier than 4.1 for CephFS-NFS back ends

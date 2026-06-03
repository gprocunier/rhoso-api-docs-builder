# Compute (nova)

RHOSO version: `18.0`
OpenStack release: `2023.1` `Antelope`
OpenStack project: `nova`
Operator: `nova-operator`

## API Reference

- RHOSO 18.0 docs: [https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_the_compute_service_for_instance_creation/index](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/configuring_the_compute_service_for_instance_creation/index)
- OpenStack API reference: [https://docs.openstack.org/2023.1/api/index.html](https://docs.openstack.org/2023.1/api/index.html)

## Validation URIs

- Semantic URI: `https://github.com/gprocunier/rhoso-api-docs-builder/validation/18.0/apis/compute-nova/`
- GitHub tree URI: [https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/compute-nova/](https://github.com/gprocunier/rhoso-api-docs-builder/tree/main/validation/18.0/apis/compute-nova/)
- GitHub Pages URI: [https://gprocunier.github.io/rhoso-api-docs-builder/validation/18.0/apis/compute-nova/](https://gprocunier.github.io/rhoso-api-docs-builder/validation/18.0/apis/compute-nova/)

## RHOSO Notes

Provides compute resource provisioning through libvirt or ironic drivers.

## Captured Limitations

- Off-path network backends
- Custom policies without support exception
- nova-serialproxy and nova-spicehtml5proxy packages
- File injection of personality files
- Persistent memory for instances
- QEMU emulation of non-native architectures
- LVM as an image backend
- ploop image format
- NFS versions earlier than 4

# Keycloak Collection for Ansible

![](https://github.com/octo-technology/keycloak-collection/workflows/ansible-test/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/octo-technology/keycloak-collection/branch/master/graph/badge.svg)](https://codecov.io/gh/octo-technology/keycloak-collection)

This repo hosts the `inspq.keycloak` Ansible Collection.

The collection includes a variety of Ansible content to help automate the management of resources in Keycloak.

## Included content

Click on the name of a plugin or module to view that content's documentation:

  - **Connection Plugins**:
  - **Filter Plugins**:
  - **Inventory Source**:
  - **Callback Plugins**:
  - **Lookup Plugins**:
  - **Modules**:
    - keycloak_authentication
    - keycloak_client
    - keycloak_clienttemplate
    - keycloak_component
    - keycloak_group
    - keycloak_identity_provider
    - keycloak_realm
    - keycloak_role
    - keycloak_user

## Supported Keycloak versions

This collection is currently testing the modules against Keycloak versions `8.0.2` and `9.0.2`.

## Installation and Usage

### Installing the Collection

Before using the Keycloak collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install <collection_archive_path>

The archive can be downloaded from the Github release page.

### Using modules from the Keycloak Collection in your playbooks

You can either call modules by their Fully Qualified Collection Namespace (FQCN), like `inspq.keycloak.keycloak_client`, or you can call modules by their short name if you list the `inspq.keycloak` collection in the playbook's `collections`, like so:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  collections:
    - inspq.keycloak

  tasks:
    - name: Create or update Keycloak client (minimal example)
      keycloak_client
        auth_client_id: admin-cli
        auth_keycloak_url: https://auth.example.com/auth
        auth_realm: master
        auth_username: USERNAME
        auth_password: PASSWORD
        client_id: test
        state: present
        - name: Ensure Influxdb datasource exists.
          keycloak_client:
            name: "some-client"
            grafana_url: "https://grafana.company.com"
            grafana_user: "admin"
            grafana_password: "xxxxxx"
            org_id: "1"
            ds_type: "influxdb"
            ds_url: "https://influx.company.com:8086"
            database: "telegraf"
            time_interval: ">10s"
            tls_ca_cert: "/etc/ssl/certs/ca.pem"
```

For documentation on how to use individual modules and other content included in this collection, please see the links in the 'Included content' section earlier in this README.

## Testing and Development

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

You can run the collection's test suites with the commands:

    ansible-test sanity --docker -v --color
    ansible-test integration --docker -v --color

## License

GNU General Public License v3.0 or later

See LICENCE to see the full text.

## Contributing

Any contribution is welcome and we only ask contributors to:
* Provide *at least* integration tests for any contribution.
* Create an issues for any significant contribution that would change a large portion of the code base.

SSH YAML Configuration
======================

Actual Version : **1.0.2**

**SSHYC** short for SSH YAML Configuration is tool to make .ssh/config from YAML files.


* Licensed under MIT License

Features
--------

Current Features
~~~~~~~~~~~~~~~~

* Attention this tools overwrites ~/.ssh/config file
* Write ~/.ssh/config.yaml or ~/.ssh/config.yml

Examples
--------

.. code-block:: yaml

   %YAML 1.1
    ---
    all:
        ForwardAgent: 'yes'

    shared: &shared-settings
        User: test
        ForwardAgent: 'yes'

    presets:
        main: &preset--main
            ForwardAgent: 'yes'

    company:
        testuser: &company__testuser
            User: testuser

    projects:
        test:
            test_host_project:
                Hostname: test
                $Proxy: test.test

    groups:
        test_group:
            test_host:
                <<: *company__testuser
                <<: *preset--main
                Hostname: test_host.test_group.test

    host_groups:
        host_group_test.test:
            test_host:
                <<: *company__testuser
                <<: *preset--main
                Hostname: test_host.test_group.test

    hosts:
        test_host_12:
            <<: *company__testuser
            <<: *shared-settings
            Hostname: test_host12.test

Credits
---------

Created by **Patryk Adamczyk**

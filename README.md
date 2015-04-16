Overview
--------

This plugin has _only_ been tested on __OpenStack Juno__ running on top of __Ubuntu Server 14.04.1__ using __Python 2.7.6__.

This plugin is intended to be installed on every compute node in your OpenStacak environment.

Once installed, this plugin will query the OpenStack Nova API to gather the following metrics for the particular compute node the datadog-agent is running on:

* local_db
* local_db_used
* memory_mb
* memory_mb_used
* vcpus
* vcpus_used
* running_vms

Installation
------------

You will need to create or use an existing OpenStack user who has the __admin__ role. I recommend creating a new Tenant called __datadog__, creating a new user called __datadog__ with a complicated password tied to that Tenant with the __admin__ role. You will use that tenant, user, and password in the configuration file below.

The following steps need to be done on every compute node in your OpenStack environment you want to gather metrics for.

It is assumed you have already installed the datadog-agent on every compute node in your OpenStack environment.

__openstack-capacity-reporting.py__ needs to be copied to __/opt/datadog-agent/agent/checks.d__.

__openstack-capactiy-reporting.yaml__ needs to be copied to __/etc/dd-agent/conf.d__.

Open __openstack-capactiy-reporting.yaml__ in your favorite text editor and fill in the following parameters to match your environment:

* auth_url
* nova_endpoint
* tenant_name
* username
* password

Test
----

If you don't already have the packages installed, install __tornado__ with `pip` and __python-ntplib__ with `apt-get` otherwise you may encounter errors.

The first step to ensuring the plugin is working properly is to change into user __dd-agent__ home directory, `cd /opt/datadog-agent/agent`, and run the following command:

	PYTHONPATH=. python checks.d/openstack-capacity-reporting.py

No output means no errors.

Next, restart the __datadog-agent__ with the following command:

	service datadog-agent restart

If everything is working properly, the agent should restart without any problems.

Finally, run the following command to ensure the plugin really is working properly:

	/etc/init.d/datadog-agent info

There will be a __Checks__ section that lists each custom plugin. The __openstack-capacity-reporting__ plugin should be listed and should state __[OK]__.

At this point, you can tail the Datadog Agent logs, `tail -f /var/log/datadog/*.log`, to see the plugin is doing its job.

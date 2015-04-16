#!/usr/bin/env python

from checks import AgentCheck
import requests
import subprocess
import json


class OpenStackChecks(AgentCheck):
    def check(self, instance):
        os_auth_url = self.init_config.get('auth_url')
        nova_endpoint = self.init_config.get('nova_endpoint')
        tenant_name = self.init_config.get('tenant_name')
        username = self.init_config.get('username')
        password = self.init_config.get('password')

        content_type = {
                         'Content-type': 'application/json',
                         'Accept': 'text/plain'
                       }

        payload = {
                    "auth":
                    {
                      "tenantName": tenant_name,
                      "passwordCredentials":
                      {
                          "username": username,
                          "password": password
                      }
                    }
                  }

        keystone_auth = requests.post(os_auth_url,
                                      data=json.dumps(payload),
                                      headers=content_type).json()

        token = keystone_auth['access']['token']['id']

        headers_with_token = {'X-Auth-Token': '%s' % token}

        get_hostname = subprocess.Popen("hostname -f",
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

        hostname = get_hostname.communicate()[0].rstrip()

        nova_search_request = requests.get('%s/os-hypervisors/%s/search'
                                           % (nova_endpoint, hostname),
                                           headers=headers_with_token).json()

        hypervisor_id = nova_search_request['hypervisors'][0]['id']

        hypervisor_stats = requests.get('%s/os-hypervisors/%s'
                                        % (nova_endpoint, hypervisor_id),
                                        headers=headers_with_token).json()

        disk_total = hypervisor_stats['hypervisor']['local_gb']
        disk_used = hypervisor_stats['hypervisor']['local_gb_used']
        memory_total = hypervisor_stats['hypervisor']['memory_mb']
        memory_used = hypervisor_stats['hypervisor']['memory_mb_used']
        vcpus_total = hypervisor_stats['hypervisor']['vcpus']
        vcpus_used = hypervisor_stats['hypervisor']['vcpus_used']
        running_vms = hypervisor_stats['hypervisor']['running_vms']

        self.log.info("Checking local_gb %s" % disk_total)
        self.gauge('openstack.disk.total', disk_total)
        self.log.info("Checking local_gb_used %s " % disk_used)
        self.gauge('openstack.disk.used', disk_used)
        self.log.info("Checking memory_mb %s" % memory_total)
        self.gauge('openstack.memory.total', memory_total)
        self.log.info("Checking memory_mb_used %s" % memory_used)
        self.gauge('openstack.memory.used', memory_used)
        self.log.info("Checking vcpus %s" % vcpus_total)
        self.gauge('openstack.vcpus.total', vcpus_total)
        self.log.info("Checking vcpus_used %s" % vcpus_used)
        self.gauge('openstack.vcpus.used', vcpus_used)
        self.log.info("Checking running_vms %s" % running_vms)
        self.gauge('openstack.vms.running', running_vms)

if __name__ == '__main__':
    OpenStackChecks.from_yaml('/etc/dd-agent/conf.d/openstack-capacity-reporting.yaml')

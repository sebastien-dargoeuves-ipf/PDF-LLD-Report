from ipfabric import IPFClient


class DataSource:
    def __init__(self, server_url, token, snapshot_id):
        self.ipf = IPFClient(server_url, token=token, snapshot_id=snapshot_id, verify=False, timeout=15)

        # Network data summary
        self.system_url = self.ipf.base_url
        self.os_version = self.ipf.os_version
        self.snapshot_id = snapshot_id
        self.snapshot_name = self.ipf.snapshot.name
        self.network_devices = self.ipf.inventory.devices.count()
        self.network_sites = self.ipf.inventory.sites.count()

        # Management protocol data
        self.aaa_servers = self.ipf.technology.management.aaa_servers.all()
        self.ntp_sources = self.ipf.technology.management.ntp_sources.all()
        self.logging_remote = self.ipf.technology.management.logging_remote.all()
        self.snmp_trap_hosts = self.ipf.technology.management.snmp_trap_hosts.all()
        self.netflow_collectors = self.ipf.technology.management.netflow_collectors.all()
        self.sflow_collectors = self.ipf.technology.management.sflow_collectors.all()
        self.dns_resolver_servers = self.ipf.technology.management.dns_resolver_servers.all()







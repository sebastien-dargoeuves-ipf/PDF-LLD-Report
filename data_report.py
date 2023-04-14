from jinja2 import Environment, FileSystemLoader
from src.data_source import DataSource
from src.data_source import PathSimulation

import pdfkit


def main():
    # Initialize DataSource with server_url and token
    token = ''  # netsim
    server_url = 'https://10.194.50.22/'  # netsim

    data_source = DataSource(server_url, token, '$last')
    data_source_prev = DataSource(server_url, token, '$prev')

    # Set up the Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('src/template.html')

    path_params_list = [
        {
            'Name': 'APP server to LAN2',
            'Source IP': '172.16.1.20',
            'Destination IP': '172.16.2.20',
            'Source port': '1024-65535',
            'Destination port': '80,443',
            'Snapshot ID': '$last',
            'Protocol': 'tcp',
            'TTL': 64
        },
        {
            'Name': 'Node1 to Node2 over VXLAN',
            'Source IP': '172.16.5.21',
            'Destination IP': '172.16.5.20',
            'Source port': '1024-65535',
            'Destination port': '80',
            'Snapshot ID': '$last',
            'Protocol': 'tcp',
            'TTL': 64
        },
    ]

    path_context = []
    for path_def in path_params_list:
        ipf_path = PathSimulation(server_url2, token2, path_def)
        ipf_path_svg = ipf_path.response_svg.text
        path_context.append({**path_def, **{'path_overview': ipf_path_svg}})

    # Prepare the data to be inserted into the template
    context = {

        # Network data summary
        'system_url': data_source.system_url,
        'os_version': data_source.os_version,
        'snapshot_id': data_source.snapshot_id,
        'snapshot_id_prev': data_source_prev.snapshot_id,
        'snapshot_name': data_source.snapshot_name,
        'snapshot_name_prev': data_source_prev.snapshot_name,
        'network_devices': data_source.network_devices,
        'network_devices_delta': data_source.network_devices - data_source_prev.network_devices,
        'network_interfaces': data_source.network_interfaces,
        'network_interfaces_delta': data_source.network_interfaces - data_source_prev.network_interfaces,
        'network_sites': data_source.network_sites,
        'network_sites_delta': data_source.network_sites - data_source_prev.network_sites,
        'network_hosts': data_source.network_hosts,
        'network_hosts_delta': data_source.network_hosts - data_source_prev.network_hosts,

        # Network vendors
        'vendors': data_source.get_vendors(),
        'vendors_prev': data_source_prev.get_vendors(),

        # Interfaces overview
        'interfaces_active': data_source.interfaces_active,
        'interfaces_active_delta': data_source.interfaces_active - data_source_prev.interfaces_active,
        'interfaces_edge': data_source.interfaces_edge,
        'interfaces_edge_delta': data_source.interfaces_edge - data_source_prev.interfaces_edge,
        'interfaces_switchport': data_source.interfaces_switchport,
        'interfaces_switchport_delta': data_source.interfaces_switchport - data_source_prev.interfaces_switchport,
        'interfaces_channels': data_source.interfaces_channels,
        'interfaces_channels_delta': data_source.interfaces_channels - data_source_prev.interfaces_channels,
        'interfaces_tunnels_ipv4': data_source.interfaces_tunnels_ipv4,
        'interfaces_tunnels_ipv4_delta': data_source.interfaces_tunnels_ipv4 - data_source_prev.interfaces_tunnels_ipv4,
        'interfaces_tunnels_ipv6': data_source.interfaces_tunnels_ipv6,
        'interfaces_tunnels_ipv6_delta': data_source.interfaces_tunnels_ipv6 - data_source_prev.interfaces_tunnels_ipv6,
        'ipsec_gateways': data_source.ipsec_gateways,
        'ipsec_gateways_delta': data_source.ipsec_gateways - data_source_prev.ipsec_gateways,
        'ipsec_tunnels': data_source.ipsec_tunnels,
        'ipsec_tunnels_delta': data_source.ipsec_tunnels - data_source_prev.ipsec_tunnels,

        # Addressing overview
        'managed_networks': data_source.managed_networks,
        'managed_networks_delta': data_source.managed_networks - data_source_prev.managed_networks,
        'ipv4_interfaces': data_source.ipv4_interfaces,
        'ipv4_interfaces_delta': data_source.ipv4_interfaces - data_source_prev.ipv4_interfaces,
        'ipv6_interfaces': data_source.ipv6_interfaces,
        'ipv6_interfaces_delta': data_source.ipv6_interfaces - data_source_prev.ipv6_interfaces,
        'arp': data_source.arp,
        'arp_delta': data_source.arp - data_source_prev.arp,
        'vrfs': data_source.vrfs,
        'vrfs_delta': data_source.vrfs - data_source_prev.vrfs,

        # Switching overview
        'stp_bridges': data_source.stp_bridges,
        'stp_bridges_delta': data_source.stp_bridges - data_source_prev.stp_bridges,
        'stp_instances': data_source.stp_instances,
        'stp_instances_delta': data_source.stp_instances - data_source_prev.stp_instances,
        'stp_neighbors': data_source.stp_neighbors,
        'stp_neighbors_delta': data_source.stp_neighbors - data_source_prev.stp_neighbors,
        'stp_virtual_ports': data_source.stp_virtual_ports,
        'stp_virtual_ports_delta': data_source.stp_virtual_ports - data_source_prev.stp_virtual_ports,
        'stp_vlans': data_source.stp_vlans,
        'stp_vlans_delta': data_source.stp_vlans - data_source_prev.stp_vlans,
        'vlans': data_source.vlans,
        'vlans_delta': data_source.vlans - data_source_prev.vlans,
        'mac': data_source.mac,
        'mac_delta': data_source.mac - data_source_prev.mac,

        # Routing overview
        'routes_ipv4': data_source.routes_ipv4,
        'routes_ipv4_delta': data_source.routes_ipv4 - data_source_prev.routes_ipv4,
        'routes_ipv6': data_source.routes_ipv6,
        'routes_ipv6_delta': data_source.routes_ipv6 - data_source_prev.routes_ipv6,
        'routes_multicast': data_source.routes_multicast,
        'routes_multicast_delta': data_source.routes_multicast - data_source_prev.routes_multicast,
        'routes_attached': data_source.routes_attached,
        'routes_attached_delta': data_source.routes_attached - data_source_prev.routes_attached,
        'routes_connected': data_source.routes_connected,
        'routes_connected_delta': data_source.routes_connected - data_source_prev.routes_connected,
        'routes_static': data_source.routes_static,
        'routes_static_delta': data_source.routes_static - data_source_prev.routes_static,
        'routes_bgp': data_source.routes_bgp,
        'routes_bgp_delta': data_source.routes_bgp - data_source_prev.routes_bgp,
        'routes_ospf': data_source.routes_ospf,
        'routes_ospf_delta': data_source.routes_ospf - data_source_prev.routes_ospf,
        'routes_isis': data_source.routes_isis,
        'routes_isis_delta': data_source.routes_isis - data_source_prev.routes_isis,
        'routes_eigrp': data_source.routes_eigrp,
        'routes_eigrp_delta': data_source.routes_eigrp - data_source_prev.routes_eigrp,
        'routes_rip': data_source.routes_rip,
        'routes_rip_delta': data_source.routes_rip - data_source_prev.routes_rip,

        # Wireless overview
        'wireless_controllers': data_source.stp_bridges,
        'wireless_controllers_delta': data_source.stp_bridges - data_source_prev.stp_bridges,
        'wireless_access_points': data_source.stp_virtual_ports,
        'wireless_access_points_delta': data_source.stp_virtual_ports - data_source_prev.stp_virtual_ports,
        'wireless_radios_ssid_summary': data_source.stp_instances,
        'wireless_radios_ssid_summary_delta': data_source.stp_instances - data_source_prev.stp_instances,
        'wireless_clients': data_source.stp_neighbors,
        'wireless_clients_delta': data_source.stp_neighbors - data_source_prev.stp_neighbors,

        # Path Compliance
        'path_context': path_context

    }

    # Render the HTML with the data from the DataSource instance
    html_content = template.render(context)

    # Convert the rendered HTML to a PDF
    pdfkit.from_string(html_content, 'export/report-lab.pdf')


if __name__ == "__main__":
    main()

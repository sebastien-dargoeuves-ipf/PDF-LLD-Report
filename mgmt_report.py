# Import the required modules
from src.data_source import DataSource
from src.modules import get_distribution_ratio
from src.modules import plot_pie_chart

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from weasyprint import HTML


def main():
    # Initialize DataSources with a token and server_url
    server_url = os.environ.get('NETSIM-URL')  # netsim
    token = os.environ.get('API-TOKEN')  # netsim
    snapshot_id = os.environ.get('SNAPSHOT-ID')

    data_source = DataSource(server_url, token, snapshot_id)

    # The time part
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d-%H-%M")

    # HTML, PDF and CSS file paths
    html_file_path = Path('export/' + f"MGMT-Report-{formatted_time}.html")
    pdf_file_path = Path('export/' + f"MGMT-Report-{formatted_time}.pdf")
    css_file_path = Path('src/style.css')

    # Set up the Jinja2 environment and load the HTML template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('src/template.html')

    aaa_servers = get_distribution_ratio(data_source.aaa_servers, 'ip')
    ntp_sources = get_distribution_ratio(data_source.ntp_sources, 'source')
    logging_remote = get_distribution_ratio(data_source.logging_remote, 'host')
    snmp_trap_hosts = get_distribution_ratio(data_source.snmp_trap_hosts, 'dstHost')
    netflow_collectors = get_distribution_ratio(data_source.netflow_collectors, 'collector')
    sflow_collectors = get_distribution_ratio(data_source.sflow_collectors, 'collector')
    dns_resolver_servers = get_distribution_ratio(data_source.dns_resolver_servers, 'ip')

    mgmt_proto_list = [
        {
            'name': 'AAA Servers',
            'description': 'The AAA servers configured on the network devices.',
            'server_name': 'Authentication server',
            'servers': get_distribution_ratio(data_source.aaa_servers, 'ip'),
            'plot': plot_pie_chart(aaa_servers, 'aaa'),
        },
        {
            'name': 'NTP Sources',
            'description': 'The NTP sources configured on the network devices.',
            'server_name': 'NTP source',
            'servers': ntp_sources,
            'plot': plot_pie_chart(ntp_sources, 'ntp'),
        },
        {
            'name': 'Syslog Servers',
            'description': 'The logging remote servers configured on the network devices.',
            'server_name': 'Syslog server',
            'servers': logging_remote,
            'plot': plot_pie_chart(logging_remote, 'logging'),
        },
        {
            'name': 'SNMP Trap Servers',
            'description': 'The SNMP trap hosts configured on the network devices.',
            'server_name': 'SNMP trap server',
            'servers': snmp_trap_hosts,
            'plot': plot_pie_chart(snmp_trap_hosts, 'snmp'),
        },
        {
            'name': 'NetFlow Collectors',
            'description': 'The NetFlow collectors configured on the network devices.',
            'server_name': 'NetFlow collector',
            'servers': netflow_collectors,
            'plot': plot_pie_chart(netflow_collectors, 'netflow'),
        },
        {
            'name': 'sFlow Collectors',
            'description': 'The sFlow collectors configured on the network devices.',
            'server_name': 'sFlow collector',
            'servers': sflow_collectors,
            'plot': plot_pie_chart(sflow_collectors, 'sflow'),
        },
        {
            'name': 'DNS Resolvers',
            'description': 'The DNS resolver servers configured on the network devices.',
            'server_name': 'DNS resolver',
            'servers': dns_resolver_servers,
            'plot': plot_pie_chart(dns_resolver_servers, 'dns'),
        }
    ]

    # Prepare the context data to be inserted into the HTML template
    context = {
        # Network data summary
        'os_version': data_source.os_version,
        'system_url': data_source.system_url,
        'snapshot_name': data_source.snapshot_name,
        'snapshot_id': data_source.snapshot_id,
        'network_sites': data_source.network_sites,
        'network_devices': data_source.network_devices,

        # Time
        'formatted_time': formatted_time,
        'mgmt_protocols': mgmt_proto_list,
    }

    # Save rendered HTML to a file
    with open(html_file_path, 'w') as html_file:
        html_file.write(template.render(context))

    # Save rendered PDF to a file
    HTML(html_file_path).write_pdf(
        pdf_file_path,
        stylesheets=[css_file_path]
    )


if __name__ == "__main__":
    main()

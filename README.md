# IP Fabric Data Report Generator
The Management Protocols PDF report provides an overview of the distribution of management protocols servers in the network. The data was collected using IP Fabric's SDK and includes information about the following management protocols: SNMP, NTP, sFlow, NetFlow, Syslog, AAA, and DNS.

## Requirements
* Python 3.7 or higher 
* Jinja2
* ipfabric
* weasyprint
* matplotlib

## Usage
* Clone this repository.
* Install the weasyprint module using pip install weasyprint.
* Set the appropriate values for token, server_url and snapshot_id in mgmt_report.py.
* Run the script using python mgmt_report.py.
* The generated report will be saved in export folder. Plot images will be saved in the img folder.

To use this script, you will need to provide the following parameters:

* `token`: Your API token for the IP Fabric server
* `server_url`: The URL of the IP Fabric server
* `snapshot_id`: The first snapshot ID for baseline data collection


## Data Collection
To collect data about your network, simply create an instance of the DataSource class and pass in the required parameters:

```python
from src.data_source import DataSource

server_url = "https://<IP_FABRIC_SERVER>"
token = "<API_TOKEN>"
snapshot_id = "<SNAPSHOT_ID>"

datasource = DataSource(server_url, token, snapshot_id)
```
This will create an instance of the DataSource class and populate its attributes with data about the management protocols.

## Report Contents
The report contains the following sections:

* AAA servers 
* NTP sources
* Syslog servers
* SNMP servers
* Netflow servers
* sFlow servers
* DNS servers

## License
This project is licensed under the MIT License. See the LICENSE file for details.

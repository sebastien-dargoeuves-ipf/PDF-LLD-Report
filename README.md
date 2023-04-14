# IP Fabric Data Report Generator
This Python script generates a health report for a network using data from two data sources (snapshots). It uses IP Fabric's SDK to fetch data and Jinja2 and HTML to create report, which is then exported to PDF. 

## Requirements
* Python 3.7 or higher 
* pdfkit module
* The requests library
* The ipfabric library

## Usage
* Clone this repository.
* Install the pdfkit module using pip install pdfkit.
* Set the appropriate values for token1, token2, server_url1, and server_url2 variables in main.py.
* Run the script using python main.py.
* The generated report will be saved in report-lab.pdf.

To use this script, you will need to provide the following parameters:

* `server_url`: The URL of the IP Fabric server
* `token`: Your API token for the IP Fabric server
* `snapshot_id`: The ID of the IP Fabric snapshot to use for data collection

## Data Collection
To collect data about your network, simply create an instance of the DataSource class and pass in the required parameters:

```python
from src.data_source import DataSource

server_url = "https://<IP_FABRIC_SERVER>"
token = "<API_TOKEN>"
snapshot_id = "<SNAPSHOT_ID>"

datasource = DataSource(server_url, token, snapshot_id)
```
This will create an instance of the DataSource class and populate its attributes with data about the network configuration.

## Path Simulation
To simulate a network path, create an instance of the PathSimulation class and pass in the required parameters:

```python
from src.data_source import PathSimulation

server_url = "https://<IP_FABRIC_SERVER>"
token = "<API_TOKEN>"
params = {
    "Source IP": "<SOURCE_IP>",
    "Destination IP": "<DESTINATION_IP>",
    "Protocol": "<PROTOCOL>",
    "Destination port": "<DESTINATION_PORT>",
    "Source port": "<SOURCE_PORT>",
    "TTL": "<TTL>",
    "Snapshot ID": "<SNAPSHOT_ID>"
}

path_simulator = PathSimulation(server_url, token, params)
```
This will create an instance of the PathSimulation class and send a request to the IP Fabric server to simulate a network path based on the parameters provided. The SVG image of the path will be returned in the response_svg attribute.

## Report Contents
The report contains the following sections:

* Network data summary 
* Network vendors
* Interfaces overview
* Addressing overview
* Switching overview
* Routing overview
* Wireless overview
* Path Compliance

The "Path Compliance" section contains a table for each item in the path_params_list variable in main.py.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
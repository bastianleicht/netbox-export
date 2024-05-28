# Netbox Tenant Export Script

This script will export all data from a Netbox tenant to a PDF file. The script will export the following data:

* Devices
* Locations
* Tenant Data
* Racks

## Installation

1. Clone the repository
2. Install the required packages
```bash
pip install -r requirements.txt
```

## Usage

1. Rename the `.env.example` file to `.env` and update the following variables:
```bash
NETBOX_URL=https://netbox.example.com
NETBOX_TOKEN=your-netbox-token
TENANT_NAME=your-tenant-id
```

2. Run the script
```bash
python nb_export.py
```

## ToDo

- [ ] Update the formatting of the PDF to be more visually appealing
- [ ] Update the formatting of exported interfaces
- [ ] Implement Support for VLANs on Interfaces
- [ ] Implement Support for IP Addresses on Interfaces
- [ ] Implement Support for Circuits
- [ ] Implement Support for Virtual Machines
- [ ] Implement Support for Power Feeds
- [ ] Implement Support for Power Panels

## License

This project is licensed under the BSD 2-Clause License - see the [LICENSE](LICENSE) file for details.
